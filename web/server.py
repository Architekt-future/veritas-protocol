# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import trafilatura

app = Flask(__name__)
CORS(app) # Це щоб браузер не лаявся

@app.route('/fetch', methods=['POST'])
def fetch_url():
    data = request.json
    url = data.get('url')
    
    # Завантажуємо вміст сторінки
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return jsonify({"error": "Не вдалося завантажити сторінку"}), 400
        
    # Витягуємо тільки текст (без реклами і меню)
    content = trafilatura.extract(downloaded)
    
    return jsonify({"text": content, "source": url})

if __name__ == '__main__':
    app.run(port=5000)
