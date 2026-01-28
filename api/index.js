const axios = require('axios');
const cheerio = require('cheerio');

module.exports = async (req, res) => {
    // Встановлюємо CORS заголовки для повної свободи запитів
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*'); // Дозволяє запити звідусіль
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

    // Обробка попереднього запиту (preflight request)
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    const { url } = req.query;

    // Якщо URL не вказано, просто кажемо, що ми в мережі
    if (!url) {
        return res.status(200).json({ 
            status: "online", 
            message: "Veritas Protocol API is active. Waiting for signal..." 
        });
    }

    try {
        // Спроба отримати дані з цільового сайту
        const response = await axios.get(url, { 
            timeout: 8000,
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            }
        });

        const $ = cheerio.load(response.data);
        
        // Витягуємо чистий текст, обмежуємо до 5000 символів для аналізу
        const text = $('body').text()
            .replace(/\s+/g, ' ')
            .trim()
            .substring(0, 5000);

        return res.status(200).json({
            url: url,
            content: text,
            length: text.length
        });
    } catch (error) {
        // Якщо сайт заблокував запит або впав таймаут
        return res.status(500).json({ 
            error: "Scraping failed: " + error.message,
            suggestion: "Try another URL or check if the site blocks bots."
        });
    }
};
