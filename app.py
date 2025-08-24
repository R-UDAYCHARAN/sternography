from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import numpy as np
import io
import base64
import os
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def text_to_binary(text):
    """Convert text to binary string"""
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary + '00000000'  # Add null terminator

def binary_to_text(binary):
    """Convert binary string back to text"""
    # Ensure binary string length is a multiple of 8
    if len(binary) % 8 != 0:
        # Pad with zeros if necessary
        binary = binary.ljust((len(binary) + 7) // 8 * 8, '0')
    
    text = ""
    valid_chars = 0
    total_chars = 0
    
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            try:
                char_code = int(byte, 2)
                total_chars += 1
                # Only add printable characters
                if 32 <= char_code <= 126:
                    text += chr(char_code)
                    valid_chars += 1
                else:
                    # If we encounter non-printable characters, this might not be valid text
                    break
            except ValueError:
                continue
    
    # Check if we have a reasonable amount of valid characters
    if total_chars > 0 and valid_chars / total_chars < 0.8:
        return ""
    
    return text

def hide_text_in_image(image, text):
    """Hide text in image using LSB steganography"""
    # Convert text to binary
    binary_text = text_to_binary(text)
    
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Check if image can hold the text
    if len(binary_text) > img_array.size:
        raise ValueError("Text too long for this image")
    
    # Flatten the image array
    flat_img = img_array.flatten()
    
    # Hide the binary text in the least significant bits
    for i, bit in enumerate(binary_text):
        flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
    
    # Reshape back to original dimensions
    stego_img = flat_img.reshape(img_array.shape)
    
    return Image.fromarray(stego_img.astype(np.uint8))

def extract_text_from_image(image):
    """Extract hidden text from image"""
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Flatten the image array
    flat_img = img_array.flatten()
    
    # Extract binary text from least significant bits
    binary_text = ""
    for i in range(len(flat_img)):
        bit = flat_img[i] & 1
        binary_text += str(bit)
        
        # Check for null terminator (8 consecutive zeros)
        if len(binary_text) >= 8 and binary_text[-8:] == '00000000':
            # Remove the null terminator
            binary_text = binary_text[:-8]
            break
    
    # Convert binary back to text
    text = binary_to_text(binary_text)
    
    # Additional validation: check if the text looks like meaningful content
    if text:
        # Check if text contains mostly alphanumeric characters and common punctuation
        valid_chars = sum(1 for c in text if c.isalnum() or c in ' .,!?-_\'\"')
        if len(text) > 0 and valid_chars / len(text) < 0.7:
            return ""
        
        # Check if text is too short (likely noise)
        if len(text) < 2:
            return ""
    
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hide', methods=['POST'])
def hide_text():
    try:
        # Get uploaded image and text
        image_file = request.files['image']
        text = request.form['text']
        
        if not image_file or not text:
            return jsonify({'error': 'Please provide both image and text'}), 400
        
        # Check file size (limit to 10MB)
        image_file.seek(0, 2)  # Go to end
        file_size = image_file.tell()
        image_file.seek(0)  # Reset to beginning
        
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            return jsonify({'error': 'Image file too large. Please use an image smaller than 10MB.'}), 400
        
        # Open and process image
        image = Image.open(image_file.stream)
        
        # Resize large images to prevent timeout
        max_size = 2048
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Hide text in image
        stego_image = hide_text_in_image(image, text)
        
        # Save to disk first
        timestamp = int(time.time())
        filename = f"steganographed_{timestamp}.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        stego_image.save(filepath, 'PNG', optimize=True)
        
        # Return file path instead of base64 for better performance
        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/download/{filename}',
            'message': 'Text hidden successfully!'
        })
        
    except Exception as e:
        print(f"Hide error: {str(e)}")
        return jsonify({'error': f'Error processing image: {str(e)}'}), 400

@app.route('/extract', methods=['POST'])
def extract_text():
    try:
        # Get uploaded image
        image_file = request.files['image']
        
        if not image_file:
            return jsonify({'error': 'Please provide an image'}), 400
        
        # Check file size (limit to 10MB)
        image_file.seek(0, 2)  # Go to end
        file_size = image_file.tell()
        image_file.seek(0)  # Reset to beginning
        
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            return jsonify({'error': 'Image file too large. Please use an image smaller than 10MB.'}), 400
        
        # Open and process image
        image = Image.open(image_file.stream)
        
        # Resize large images to prevent timeout
        max_size = 2048
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text from image
        hidden_text = extract_text_from_image(image)
        
        print(f"Extracted text: '{hidden_text}' (length: {len(hidden_text)})")
        
        if not hidden_text:
            return jsonify({'error': 'No hidden text found in this image. This image either contains no hidden text or the text was not hidden using this tool.'}), 400
        
        return jsonify({
            'success': True,
            'text': hidden_text,
            'message': 'Text extracted successfully!'
        })
        
    except Exception as e:
        print(f"Extraction error: {str(e)}")
        return jsonify({'error': f'Error extracting text: {str(e)}'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    """Download a file from the uploads directory"""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True) 