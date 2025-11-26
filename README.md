# PDF to MP3 Converter

A simple web application that converts PDF documents to MP3 audio files using text-to-speech technology.

## Features

- 📄 Upload PDF files (up to 16MB)
- 🗣️ Convert text to speech in multiple languages
- 🎧 Download generated MP3 files
- 🎨 Beautiful, responsive UI
- 📱 Mobile-friendly design

## Supported Languages

- English
- Spanish
- French
- German
- Italian
- Portuguese
- Arabic
- Hindi
- Chinese (Simplified)
- Japanese

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Clone or download this project**

2. **Install required Python packages:**

```bash
pip install flask gtts PyPDF2
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## Project Structure

```
pdf-to-mp3-converter/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/
│   └── index.html        # Main HTML template
│
├── static/
│   ├── style.css         # Stylesheet
│   └── app.js            # JavaScript functionality
│
├── uploads/              # Temporary PDF storage (auto-created)
└── output/               # Generated MP3 files (auto-created)
```

## Usage

1. **Start the application:**

```bash
python app.py
```

2. **Open your browser and navigate to:**

```
http://localhost:5000
```

3. **Convert a PDF:**
   - Click the upload area or drag and drop a PDF file
   - Select your preferred language
   - Click "Convert to MP3"
   - Wait for processing to complete
   - Download your MP3 file

## How It Works

1. User uploads a PDF file through the web interface
2. The Flask backend extracts text from the PDF using PyPDF2
3. The extracted text is converted to speech using Google Text-to-Speech (gTTS)
4. The MP3 file is generated and made available for download
5. Temporary files are automatically cleaned up

## Requirements.txt

Create a `requirements.txt` file with the following content:

```
Flask==3.0.0
gTTS==2.4.0
PyPDF2==3.0.1
```

## Configuration

You can modify these settings in `app.py`:

- **MAX_CONTENT_LENGTH**: Maximum file size (default: 16MB)
- **UPLOAD_FOLDER**: Directory for temporary PDF storage
- **OUTPUT_FOLDER**: Directory for generated MP3 files

## Security Notes

- File size is limited to 16MB to prevent abuse
- Only PDF files are accepted
- Uploaded files are processed and deleted immediately
- Output files can be manually cleaned up

## Troubleshooting

### "No module named 'flask'" error
```bash
pip install flask
```

### "No module named 'gtts'" error
```bash
pip install gtts
```

### "No module named 'PyPDF2'" error
```bash
pip install PyPDF2
```

### PDF text extraction issues
- Ensure your PDF contains selectable text (not scanned images)
- Try OCR preprocessing for scanned PDFs

### Port already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Limitations

- PDFs must contain extractable text (not scanned images without OCR)
- File size limited to 16MB
- Processing time depends on PDF size
- Internet connection required for gTTS (Google Text-to-Speech)

## Future Enhancements

- [ ] Add OCR support for scanned PDFs
- [ ] Multiple voice options
- [ ] Speed and pitch controls
- [ ] Batch conversion
- [ ] Progress tracking for large files
- [ ] User authentication
- [ ] Cloud storage integration

## License

This project is open source and available for personal and educational use.

## Credits

- **Flask**: Web framework
- **gTTS**: Google Text-to-Speech
- **PyPDF2**: PDF text extraction

## Support

For issues or questions, please check:
- Python version compatibility
- Package installations
- File permissions for upload/output folders

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

To run in production, use a production server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

**Happy Converting! 🎵**