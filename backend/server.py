from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/endpoint', methods=['POST'])
def handle_data():
    data = request.json  # Extract JSON data from request body
    print("Received data:", data)
    # Process the received data as needed
    # You can also return a response to the client if needed
    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
