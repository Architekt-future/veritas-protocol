const axios = require('axios');
const cheerio = require('cheerio');

module.exports = async (req, res) => {
    // 1. Броньовані CORS-заголовки (дозволяють доступ будь-звідки)
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader('Access-Control-Allow-Headers', '*');

    // 2. Обробка Preflight запиту (браузери часто його шлють перед основним)
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    const { url } = req.query;

    // 3. Перевірка статусу (якщо просто відкрити API в браузері)
    if (!url) {
        return res.status(200).json({ 
            status: "online", 
            message: "Veritas Protocol API is active. Waiting for URL..." 
        });
    }

    try {
        // 4. Отримання даних з цільового сайту
        const response = await axios.get(url, { 
            timeout: 10000, // Чекаємо до 10 секунд
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        });

        try {
        const response = await axios.get(url, { 
            timeout: 10000,
            headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' }
        });

        const $ = cheerio.load(response.data);
        
        // --- КРОК 1: ВИДАЛЯЄМО СМІТТЯ ---
        $('script, style, .mw-empty-elt, .infobox, .navbox, .reference, .hatnote').remove();

        // --- КРОК 2: ШУКАЄМО КОНТЕНТ ---
        const mainContent = $('#mw-content-text, article, main, .article-body').first();
        let cleanText = mainContent.length ? mainContent.text() : $('body').text();

        // --- КРОК 3: ФІНАЛЬНА ЧИСТКА ---
        cleanText = cleanText
            .replace(/\s+/g, ' ') // прибираємо зайві пробіли та переноси
            .replace(/\{[^}]+\}/g, '') // видаляємо залишки CSS-коду в дужках
            .trim()
            .substring(0, 5000);

        return res.status(200).json({
            url: url,
            content: cleanText,
            length: cleanText.length
        });

    } catch (error) {
        // 6. Обробка помилок (якщо сайт лежить або блокує бота)
        return res.status(500).json({ 
            error: "Scraping failed: " + error.message 
        });
    }
};
