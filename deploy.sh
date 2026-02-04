#!/bin/bash
# Veritas Deployment Script - очищення кешу і перезапуск

echo "🧹 Очищення Python кешу..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Кеш очищено!"

echo "🔄 Перезапуск сервісу..."
# Render автоматично перезапускає після git push
# але можна форсувати через API якщо потрібно

echo "🎉 Deployment завершено!"
echo ""
echo "⚠️  ВАЖЛИВО: Після deployment:"
echo "   1. Зачекайте 30 секунд"
echo "   2. Відкрийте сайт у НОВІЙ ІНКОГНІТО вкладці"
echo "   3. Перевірте тестові тексти"
