from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/endpoint/upload": {"origins": "http://127.0.0.1:5173"}})

UPLOAD_FOLDER = 'api/endpoint/extract'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/api/endpoint/extract', methods=['POST'])
def extract_data():
    data = request.json  # Extract JSON data from request body
    # print("Received data:", data)
    # Process the received data as needed
    # You can also return a response to the client if needed
    return jsonify({'message': 'Data received successfully'})

@app.route('/api/endpoint/upload', methods=['POST'])
def upload_file():
    if 'pptxFile' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['pptxFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    
    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
