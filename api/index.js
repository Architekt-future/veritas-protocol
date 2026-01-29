const axios = require('axios');
const cheerio = require('cheerio');

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Handle POST (manual text input)
  if (req.method === 'POST') {
    try {
      const { text, source } = req.body;
      
      if (!text) {
        return res.status(400).json({ error: "No text provided" });
      }

      return res.status(200).json({
        url: source || "manual-input",
        content: text.substring(0, 10000), // Allow more text
        length: text.length,
        mode: "manual"
      });
    } catch (error) {
      return res.status(500).json({ error: "POST failed: " + error.message });
    }
  }

  // Handle GET (URL scraping)
  const { url } = req.query;

  if (!url) {
    return res.status(200).json({ 
      status: "online", 
      message: "Veritas Protocol API is active. Use ?url= or POST with text" 
    });
  }

  try {
    // Improved scraping with better timeout and headers
    const response = await axios.get(url, { 
      timeout: 15000, // Increased to 15 seconds
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
      }
    });

    const $ = cheerio.load(response.data);
    
    // Remove unwanted elements before extraction
    $('script').remove();
    $('style').remove();
    $('nav').remove();
    $('header').remove();
    $('footer').remove();
    $('iframe').remove();
    $('.advertisement').remove();
    $('.ads').remove();
    
    // Try multiple selectors for better content extraction
    let text = '';
    
    // Priority 1: Article content
    const article = $('article').text().trim();
    if (article && article.length > 100) {
      text = article;
    }
    
    // Priority 2: Main content
    if (!text) {
      const main = $('main').text().trim();
      if (main && main.length > 100) {
        text = main;
      }
    }
    
    // Priority 3: Content div
    if (!text) {
      const content = $('.content, .post-content, .entry-content, .article-content').text().trim();
      if (content && content.length > 100) {
        text = content;
      }
    }
    
    // Fallback: Body text
    if (!text) {
      text = $('body').text().trim();
    }
    
    // Clean up whitespace
    text = text.replace(/\s+/g, ' ').trim();
    
    // Allow more text (10000 chars instead of 2000)
    const finalText = text.substring(0, 10000);

    return res.status(200).json({
      url: url,
      content: finalText,
      length: finalText.length,
      mode: "scraped"
    });
  } catch (error) {
    return res.status(500).json({ 
      error: "Failed to scrape: " + error.message,
      url: url
    });
  }
};
