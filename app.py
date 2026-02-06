"""
Veritas Protocol - Flask API v13.3
Forces fresh import of Veritas modules on every restart
"""

import sys
import os

# CRITICAL: Clear module cache to force reload
print("🔄 Veritas v13.3 - Clearing module cache...")
modules_to_clear = [k for k in sys.modules.keys() if k.startswith('veritas_')]
for module in modules_to_clear:
    del sys.modules[module]
print(f"✅ Cache cleared. Loading fresh Veritas v13.3 modules...")

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__)
CORS(app)

# Initialize Veritas engine
engine = VeritasCalibratedCore()
print("✅ Veritas engine initialized")
print(f"   Pattern boost: {engine.pattern_boost_engine is not None}")
print(f"   Void detector: {engine.void_detector is not None}")
print(f"   Absurdity detector: {engine.absurdity_detector is not None}")
print(f"   Insight detector: {engine.insight_detector is not None}")

@app.route('/')
def home():
    """Serve the HTML interface"""
    try:
        return send_file('index.html')
    except:
        return jsonify({
            'status': 'online',
            'version': 'v13.3',
            'message': 'Veritas Protocol API is running (index.html not found)',
            'features': {
                'pattern_boost': engine.pattern_boost_engine is not None,
                'void_detector': engine.void_detector is not None,
                'absurdity_detector': engine.absurdity_detector is not None,
                'insight_detector': engine.insight_detector is not None,
            }
        })

@app.route('/api/analyze', methods=['GET', 'POST'])
def analyze():
    try:
        # GET request = health check
        if request.method == 'GET':
            return jsonify({
                'status': 'online',
                'version': 'v13.3',
                'modules': {
                    'pattern_boost': engine.pattern_boost_engine is not None,
                    'void_detector': engine.void_detector is not None,
                    'absurdity_detector': engine.absurdity_detector is not None,
                    'insight_detector': engine.insight_detector is not None,
                }
            })
        
        # POST request = analyze text
        data = request.get_json() or {}
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                'error': 'No text provided',
                'status': 'error'
            }), 400
        
        # Analyze text
        result = engine.analyze(text)
        return jsonify(result)
    
    except Exception as e:
        import traceback
        print(f"❌ Error in analyze: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'version': 'v13.3'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
