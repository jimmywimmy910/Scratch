from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Scratch account credentials from a text file
def load_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            username, password = line.strip().split(':')
            credentials[username] = password
    return credentials

scratch_accounts = load_credentials('credentials.txt')

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
        link = f'https://scratch-x03s.onrender.com/uploads/{file.filename}'
        return jsonify({'link': link}), 200

    return jsonify({'error': 'File upload failed'}), 500

if __name__ == '__main__':
        app.run(debug=True)
