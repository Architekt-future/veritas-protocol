from flask import Flask, request, jsonify
from flask_cors import CORS
from veritas_core import VeritasCore

app = Flask(__name__)
CORS(app)  # Дозволяє запити з Vercel
core = VeritasCore()

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    result = core.evaluate_integrity(data['text'], data.get('source', 'Unknown'))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
