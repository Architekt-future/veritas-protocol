#!/bin/bash
# Veritas v13.3 Deployment Script
# Очищує Python кеш і готує систему до перезапуску
# v13.3: Added SEMANTIC VOID detection category

set -e  # Exit on error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Veritas v13.3 Deployment Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Clean Python cache
echo "🧹 Step 1/3: Cleaning Python cache..."
echo "   Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing .pyc files..."
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

echo "   ✅ Python cache cleared!"
echo ""

# Step 2: Verify Veritas files exist
echo "📁 Step 2/3: Verifying Veritas files..."
REQUIRED_FILES=(
    "veritas_calibrated_core.py"
    "veritas_pattern_boost.py"
    "veritas_semantic_void.py"
    "veritas_absurdity_detector.py"
    "veritas_insight_density.py"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (MISSING!)"
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo ""
    echo "   ⚠️  WARNING: ${#MISSING_FILES[@]} file(s) missing!"
    echo "   Please upload: ${MISSING_FILES[*]}"
    echo ""
else
    echo "   ✅ All Veritas files present!"
fi
echo ""

# Step 3: Prepare for restart
echo "🔄 Step 3/3: Preparing for restart..."
echo "   Setting Python flags..."
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export VERITAS_VERSION=v13.3

echo "   ✅ Environment configured!"
echo ""

# Final message
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Deployment preparation complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Next steps:"
echo "   1. Service will restart automatically"
echo "   2. Wait 30 seconds after restart"
echo "   3. Test in a NEW incognito tab"
echo "   4. Verify tests pass (see DEPLOYMENT_GUIDE.md)"
echo ""
echo "🧪 Critical tests:"
echo "   • Reptiloids → CRITICAL (entropy ≥ 0.8)"
echo "   • Real science → VERIFIED (entropy ≤ 0.15)"
echo "   • Casuistry → CRITICAL (entropy ≥ 0.8)"
echo "   • Empty fluff → VOID (entropy ≥ 0.6 + void_score ≥ 0.4)"
echo ""
echo "🆕 v13.3 Changes:"
echo "   • Added SEMANTIC VOID category"
echo "   • High entropy + low content = VOID (not CRITICAL)"
echo "   • Detects 'water' texts (много слів, мало змісту)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
