// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const convertBtn = document.getElementById('convertBtn');
const languageSelect = document.getElementById('language');
const statusSection = document.getElementById('statusSection');
const statusMessage = document.getElementById('statusMessage');
const progressFill = document.getElementById('progressFill');
const resultSection = document.getElementById('resultSection');
const textPreview = document.getElementById('textPreview');
const downloadBtn = document.getElementById('downloadBtn');
const convertAnotherBtn = document.getElementById('convertAnotherBtn');

let selectedFile = null;
let mp3Filename = null;

// Upload area click handler
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File input change handler
fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Drag and drop handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFile(e.dataTransfer.files[0]);
});

// Handle file selection
function handleFile(file) {
    if (!file) return;
    
    if (file.type !== 'application/pdf') {
        showError('Please select a valid PDF file');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) {
        showError('File size exceeds 16MB limit');
        return;
    }
    
    selectedFile = file;
    uploadArea.querySelector('.upload-text').textContent = file.name;
    uploadArea.querySelector('.upload-subtext').textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
    convertBtn.disabled = false;
}

// Convert button handler
convertBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    convertBtn.disabled = true;
    showStatus('Processing your PDF...');
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('language', languageSelect.value);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Conversion failed');
        }
        
        mp3Filename = data.mp3_filename;
        showResult(data.text_preview);
        
    } catch (error) {
        showError(error.message);
        convertBtn.disabled = false;
    }
});

// Download button handler
downloadBtn.addEventListener('click', () => {
    if (mp3Filename) {
        window.location.href = `/download/${mp3Filename}`;
    }
});

// Convert another button handler
convertAnotherBtn.addEventListener('click', () => {
    // Clean up previous file
    if (mp3Filename) {
        fetch('/cleanup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: mp3Filename })
        });
    }
    
    // Reset UI
    selectedFile = null;
    mp3Filename = null;
    fileInput.value = '';
    uploadArea.querySelector('.upload-text').textContent = 'Click to upload or drag and drop';
    uploadArea.querySelector('.upload-subtext').textContent = 'PDF files only (max 16MB)';
    convertBtn.disabled = true;
    statusSection.style.display = 'none';
    resultSection.style.display = 'none';
});

// Show status
function showStatus(message) {
    statusSection.style.display = 'block';
    resultSection.style.display = 'none';
    statusMessage.textContent = message;
    progressFill.style.width = '100%';
}

// Show result
function showResult(preview) {
    statusSection.style.display = 'none';
    resultSection.style.display = 'block';
    textPreview.textContent = preview;
}

// Show error
function showError(message) {
    statusSection.style.display = 'block';
    statusMessage.innerHTML = `<div class="error">❌ ${message}</div>`;
    progressFill.style.width = '0%';
}