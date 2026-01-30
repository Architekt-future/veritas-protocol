import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

# Це змушує Render показувати твій index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Це твій бекенд, який тепер працює БЕЗ папки api
@app.route('/api/analyze', methods=['POST', 'GET'])
def analyze():
    if request.method == 'GET':
        return jsonify({"status": "online", "service": "Veritas Render Node"})
        
    try:
        data = request.json
        text = data.get('text', '')
        
        engine = VeritasCalibratedCore()
        result = engine.evaluate_integrity(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
