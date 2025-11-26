from flask import Flask, render_template, request, jsonify, send_file
from gtts import gTTS
import PyPDF2
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}

# Create necessary folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")
    return text

def text_to_speech(text, output_path, language='en'):
    """Convert text to speech and save as MP3"""
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_path)
    except Exception as e:
        raise Exception(f"Error converting to speech: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a PDF file'}), 400
    
    try:
        # Save uploaded PDF
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
        file.save(pdf_path)
        
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        
        if not text.strip():
            os.remove(pdf_path)
            return jsonify({'error': 'No text found in PDF'}), 400
        
        # Get language from request (default to English)
        language = request.form.get('language', 'en')
        
        # Convert to MP3
        mp3_filename = f"{unique_id}.mp3"
        mp3_path = os.path.join(app.config['OUTPUT_FOLDER'], mp3_filename)
        text_to_speech(text, mp3_path, language)
        
        # Clean up PDF file
        os.remove(pdf_path)
        
        return jsonify({
            'success': True,
            'message': 'Conversion successful',
            'mp3_filename': mp3_filename,
            'text_preview': text[:500] + ('...' if len(text) > 500 else '')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        return send_file(file_path, as_attachment=True, download_name=f"converted_{filename}")
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@app.route('/cleanup', methods=['POST'])
def cleanup():
    """Clean up old files"""
    try:
        data = request.json
        filename = data.get('filename')
        if filename:
            file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)