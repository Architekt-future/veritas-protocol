const axios = require('axios');
const cheerio = require('cheerio');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const { url, text } = req.method === 'POST' ? req.body : req.query;
    let content = text || '';

    // 1. Скрапінг, якщо передано URL
    if (url) {
      const response = await axios.get(url, { 
        headers: { 'User-Agent': 'Mozilla/5.0' },
        timeout: 5000 
      });
      const $ = cheerio.load(response.data);
      $('script, style, nav, footer, header').remove();
      content = $('article, main, body').text();
    }

    if (!content || content.length < 10) {
      return res.status(400).json({ error: 'Контент занадто короткий для аналізу' });
    }

    // 2. Очищення тексту для аналізу
    const cleanText = content
      .replace(/[0-9]/g, '')
      .replace(/[^а-яіїєґa-z\s]/gi, ' ')
      .toLowerCase();

    const words = cleanText.split(/\s+/).filter(w => w.length > 3);

    // 3. СУВОРА МАТЕМАТИЧНА ЕНТРОПІЯ (Алгоритм Veritas Core)
    const wordCounts = {};
    words.forEach(w => wordCounts[w] = (wordCounts[w] || 0) + 1);

    let entropy = 0;
    const totalWords = words.length;

    for (const word in wordCounts) {
      const p = wordCounts[word] / totalWords;
      entropy -= p * Math.log2(p);
    }

    // НОРМАЛІЗАЦІЯ (Корекція під живу мову)
    // Наукові тексти (Вікі) мають бути 0.5-0.7
    // Рандомний шум (Борщ) - 0.9-1.0
    const idealLog = Math.log2(totalWords);
    // Використовуємо логарифмічне згладжування, щоб великі тексти не "злітали"
    let score = entropy / (idealLog * 0.88); 
    
    // Фінальне калібрування
    const finalScore = Math.min(Math.max(score, 0.3), 1.0).toFixed(3);

    return res.status(200).json({
      status: 'online',
      content: content.substring(0, 1000) + '...', // для прев'ю
      entropy: parseFloat(finalScore),
      stats: {
        words: totalWords,
        unique: Object.keys(wordCounts).length,
        chars: content.length
      }
    });

  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({ error: 'Помилка сервера при аналізі' });
  }
};
