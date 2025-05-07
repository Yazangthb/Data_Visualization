from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the frontend

# In-memory list to store received packages.
packages = []

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    packages.append(data)
    print("Received package:", data)
    return jsonify({'status': 'success'}), 200

@app.route('/packages', methods=['GET'])
def get_packages():
    return jsonify(packages), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
