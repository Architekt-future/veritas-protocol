#!/bin/bash
# Clear Python cache before starting the app
# This ensures Render uses fresh .py files, not cached .pyc

echo "рџ§№ Clearing Python cache..."

# Remove all .pyc files
find . -type f -name "*.pyc" -delete
echo "вњ“ Removed .pyc files"

# Remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "вњ“ Removed __pycache__ directories"

# Remove .pytest_cache if exists
if [ -d ".pytest_cache" ]; then
    rm -rf .pytest_cache
    echo "вњ“ Removed .pytest_cache"
fi

echo "вњ… Cache cleared! Starting app..."
