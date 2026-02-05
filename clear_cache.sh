#!/bin/bash
# Clear Python cache before starting the app
# This ensures Render uses fresh .py files, not cached .pyc

echo "🧹 Clearing Python cache..."

# Remove all .pyc files
find . -type f -name "*.pyc" -delete
echo "✓ Removed .pyc files"

# Remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "✓ Removed __pycache__ directories"

# Remove .pytest_cache if exists
if [ -d ".pytest_cache" ]; then
    rm -rf .pytest_cache
    echo "✓ Removed .pytest_cache"
fi

echo "✅ Cache cleared! Starting app..."
