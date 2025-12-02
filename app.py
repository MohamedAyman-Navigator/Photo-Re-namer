import os
import re
import cv2
import easyocr
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import shutil
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RENAMED_FOLDER = 'renamed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RENAMED_FOLDER'] = RENAMED_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RENAMED_FOLDER, exist_ok=True)

# Initialize EasyOCR reader (load once)
print("Loading EasyOCR model...")
reader = easyocr.Reader(['en'], gpu=False)
print("EasyOCR model loaded.")

def get_code_from_image(image_path):
    """
    Reads text from the top part of the image and tries to find a numeric code (5+ digits).
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
        
        height, width, _ = img.shape
        # Crop top 30%
        crop_img = img[0:int(height*0.3), 0:width]
        
        # Read text
        result = reader.readtext(crop_img, detail=0)
        
        for text in result:
            clean_text = text.strip()
            clean_text = re.sub(r'[^\w]', '', clean_text)
            
            if clean_text.isdigit() and len(clean_text) >= 5:
                return clean_text
            
        return None
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('files[]')
    results = []
    
    # Clear previous renamed files to avoid confusion in zip
    # (Optional: in a real app, use unique session IDs)
    for f in os.listdir(app.config['RENAMED_FOLDER']):
        os.remove(os.path.join(app.config['RENAMED_FOLDER'], f))

    for file in files:
        if file.filename == '':
            continue
            
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process image
            code = get_code_from_image(filepath)
            
            if code:
                ext = os.path.splitext(filename)[1]
                new_filename = f"{code}{ext}"
                new_filepath = os.path.join(app.config['RENAMED_FOLDER'], new_filename)
                
                # Copy instead of move to keep original in uploads for reference if needed
                shutil.copy2(filepath, new_filepath)
                
                results.append({
                    'original': filename,
                    'new': new_filename,
                    'status': 'success'
                })
            else:
                results.append({
                    'original': filename,
                    'new': None,
                    'status': 'failed (no code found)'
                })
                
    return jsonify({'results': results})

@app.route('/download-all')
def download_all():
    # Create a zip of the renamed folder
    zip_filename = "renamed_photos.zip"
    zip_path = os.path.join(app.config['RENAMED_FOLDER'], zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(app.config['RENAMED_FOLDER']):
            for file in files:
                if file != zip_filename:
                    zipf.write(os.path.join(root, file), file)
                    
    return send_file(zip_path, as_attachment=True)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['RENAMED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
