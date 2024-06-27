from flask import Flask, request, jsonify
import os
import random
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Scratch account credentials from a text file
def load_credentials(file_path):
    credentials = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            username, password = line.strip().split(':')
            credentials.append((username, password))
    return credentials

scratch_accounts = load_credentials('credentials.txt')

# Function to upload project to Scratch using the Scratch API
def upload_to_scratch(file_path, username, password):
    # Implement the Scratch API login and upload logic here
    login_url = "https://scratch.mit.edu/login/"
    project_url = "https://scratch.mit.edu/upload/"

    session = requests.Session()
    # Perform login (this part may need to be adjusted based on the Scratch API)
    login_data = {
        'username': username,
        'password': password
    }
    session.post(login_url, data=login_data)

    # Upload the project
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = session.post(project_url, files=files)

    if response.status_code == 200:
        return response.json().get('project_url')
    else:
        return None

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

        # Select a random Scratch account for uploading
        username, password = random.choice(scratch_accounts)
        project_url = upload_to_scratch(file_path, username, password)

        if project_url:
            return jsonify({'link': project_url}), 200
        else:
            return jsonify({'error': 'Failed to upload to Scratch'}), 500

    return jsonify({'error': 'File upload failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
