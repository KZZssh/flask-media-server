# app.py
from flask import Flask, request, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'media'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '✅ Flask photo server is running!'

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'Photo not found'}), 400ttt

    photo = request.files['photo']
    filename = secure_filename(photo.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    photo.save(save_path)

    # ✅ Хостты енді ENV арқылы аламыз
    host = os.getenv("MEDIA_HOST", "http://localhost:5000")
    return jsonify({'url': f'{host}/media/{filename}'})

@app.route('/media/<path:filename>')
def serve_photo(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    # ❗️ Кодспейс сам меняет порт на 5000 → НЕ МЕНЯЙ!
    app.run(host='0.0.0.0', port=5000, debug=True)
