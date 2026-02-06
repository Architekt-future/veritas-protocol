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
print(f"   LAC Finance: {engine.lac_finance is not None}")
print(f"   LAC Labor: {engine.lac_labor is not None}")

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
                'version': 'v13.6',
                'modules': {
                    'pattern_boost': engine.pattern_boost_engine is not None,
                    'void_detector': engine.void_detector is not None,
                    'absurdity_detector': engine.absurdity_detector is not None,
                    'insight_detector': engine.insight_detector is not None,
                    'lac_finance': engine.lac_finance is not None,
                    'lac_labor': engine.lac_labor is not None,
                }
            })
        
        # POST request = analyze text or URL
        data = request.get_json() or {}
        text = data.get('text', '')
        url = data.get('url', '')
        
        # If URL provided, scrape it
        if url and not text:
            try:
                import requests
                from bs4 import BeautifulSoup
                
                headers = {'User-Agent': 'Mozilla/5.0 (compatible; VeritasBot/1.0)'}
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Get text
                text = soup.get_text()
                
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                if not text or len(text) < 100:
                    return jsonify({
                        'error': 'Could not extract enough text from URL',
                        'status': 'error'
                    }), 400
                    
            except Exception as e:
                return jsonify({
                    'error': f'Failed to scrape URL: {str(e)}',
                    'status': 'error'
                }), 400
        
        if not text:
            return jsonify({
                'error': 'No text or URL provided',
                'status': 'error'
            }), 400
        
        # Analyze text
        result = engine.analyze(text)
        
        # Add scraped text preview if URL was provided
        if url:
            result['scraped_text_preview'] = text[:1000] if len(text) > 1000 else text
            result['scraped_text_length'] = len(text)
            result['scraped_url'] = url
        
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
