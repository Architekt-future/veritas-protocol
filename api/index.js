const axios = require('axios');
const cheerio = require('cheerio');

module.exports = async (req, res) => {
    // 1. Налаштування CORS (щоб Опера не сварилася)
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader('Access-Control-Allow-Headers', '*');

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    const { url } = req.query;

    if (!url) {
        return res.status(200).json({ status: "online", message: "Veritas Protocol API Active" });
    }

    try {
        const response = await axios.get(url, { 
            timeout: 10000,
            headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' }
        });

        const $ = cheerio.load(response.data);
        
        // --- ТУТ МАГІЯ ОЧИЩЕННЯ ---
        // Видаляємо все технічне: скрипти, стилі, навігацію, мета-дані
        $('script, style, link, meta, .mw-empty-elt, .infobox, .navbox, .reference, .hatnote, footer, nav, header').remove();

        // Шукаємо "м'ясо" статті (для Вікіпедії це #mw-content-text)
        let contentSelector = $('#mw-content-text, article, main, .article-body, .post-content').first();
        let rawText = contentSelector.length ? contentSelector.text() : $('body').text();

        // Очищаємо текст від залишків CSS-коду (все, що в фігурних дужках) та зайвих пробілів
        let cleanText = rawText
            .replace(/@media[^{]+\{[^}]+\}/g, '') // Видаляємо медіа-запити
            .replace(/\.[a-z0-9-]+[^{]+\{[^}]+\}/g, '') // Видаляємо CSS класи
            .replace(/\{[^}]+\}/g, '') // Видаляємо будь-що в фігурних дужках
            .replace(/\s+/g, ' ') // Стискаємо пробіли
            .trim()
            .substring(0, 5000);

        return res.status(200).json({
            url: url,
            content: cleanText,
            length: cleanText.length
        });

    } catch (error) {
        return res.status(500).json({ error: "Analysis failed: " + error.message });
    }
};
