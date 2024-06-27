from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'gameFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['gameFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        link = f'http://your-backend-server.com/uploads/{file.filename}'
        return jsonify({'link': link}), 200

    return jsonify({'error': 'File upload failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
