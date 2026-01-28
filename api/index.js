// Veritas Protocol - Serverless Scraper
// Deployable on Vercel

export default async function handler(req, res) {
  // CORS headers (дозволяємо requests з будь-якого домену)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const { url } = req.query;
  
  if (!url) {
    return res.status(400).json({ 
      success: false, 
      error: 'URL parameter required' 
    });
  }

  try {
    // Fetch webpage
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const html = await response.text();
    
    // Simple text extraction (without external dependencies)
    const text = html
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();

    // Extract title
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : 'Unknown Title';

    // Extract source
    const domain = new URL(url).hostname.replace('www.', '');

    return res.status(200).json({
      success: true,
      url: url,
      title: title,
      text: text.substring(0, 10000), // Limit to 10k chars
      source: domain
    });

  } catch (error) {
    return res.status(500).json({
      success: false,
      error: error.message
    });
  }
}
```

### 4.4 Прокрути вниз, у поле "Commit message" напиши:
```
Add serverless scraper
```

### 4.5 Натисни зелену кнопку: **"Commit new file"**

**✅ Файл створений!**

---

### 4.6 Тепер створи другий файл: **"Add file" → "Create new file"**

### 4.7 У полі "Name your file..." напиши:
```
vercel.json
