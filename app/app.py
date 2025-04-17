from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    output_format = request.form['format']
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    base, ext = os.path.splitext(filename)
    output_filename = f"{base}.{output_format}"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    image = Image.open(input_path)
    image.save(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
