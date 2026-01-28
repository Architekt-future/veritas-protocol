const axios = require('axios');
const cheerio = require('cheerio');

module.exports = async (req, res) => {
  // Додаємо CORS, щоб фронтенд міг звертатися до API
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const { url } = req.query;

  if (!url) {
    return res.status(200).json({ 
      status: "online", 
      message: "Veritas Protocol API is active. Please provide a URL via ?url=" 
    });
  }

  try {
    const response = await axios.get(url, { timeout: 5000 });
    const $ = cheerio.load(response.data);
    const text = $('body').text().replace(/\s+/g, ' ').trim().substring(0, 2000);

    return res.status(200).json({
      url: url,
      content: text,
      length: text.length
    });
  } catch (error) {
    return res.status(500).json({ error: "Failed to scrape: " + error.message });
  }
};
