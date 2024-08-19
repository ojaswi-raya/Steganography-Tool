from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from steganography import encode_image, decode_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['RESULT_FOLDER']):
    os.makedirs(app.config['RESULT_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        message = request.form['message']
        output_image_path = os.path.join(app.config['RESULT_FOLDER'], 'encoded_' + filename)
        
        try:
            encode_image(file_path, message, output_image_path)
            return render_template('index.html', filename='encoded_' + filename)
        except Exception as e:
            print(f"Error during encoding: {e}")
            return redirect(request.url)
    
    return redirect(request.url)

@app.route('/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            message = decode_image(file_path)
            return render_template('index.html', message=message)
        except Exception as e:
            print(f"Error during decoding: {e}")
            return redirect(request.url)
    
    return redirect(request.url)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == '__main__':
    app.run(debug=True)
