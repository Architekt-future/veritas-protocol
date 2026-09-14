#!/bin/bash
# Veritas v19.2 Pre-Start Script
# Очищує Python кеш ПЕРЕД запуском сервера
# v19.2: ARD checker, media bias, full bilingual

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Veritas v19.2 Pre-Start Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Clean Python cache
echo "🧹 Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo "✅ Python cache cleared!"
echo ""

# 14.09.2026: завантаження ваг ONNX-моделі для PREEMPTIVE_MONOPOLY_SEMANTIC
# ДО старту gunicorn — навмисно. Два попередні заходи (v1: sentence-
# transformers+torch, v2: onnxruntime без цього кроку) клали сервіс, бо
# завантаження ~150-470MB відбувалось ВСЕРЕДИНІ обробки першого живого
# запиту, на єдиному sync-воркері — той блокувався, Render health-check
# вважав сервіс мертвим і рестартував його, зациклюючи процес. Тут це
# завантаження — частина білд/старт-скрипта, до "Starting Gunicorn", тобто
# до того, як Render почне слати health-check і трафік на порт.
#
# timeout 120s — якщо мережа до huggingface.co недоступна чи повільна,
# НЕ вішаємо весь деплой навічно: даємо один шанс, і йдемо далі байдуже
# до результату. Немає директиви "має завершитись успішно" (|| true) —
# якщо не вийшло, PHASE 10b-semantic у veritas_calibrated_core.py сам
# зловить виняток при першому реальному запиті й деградує до regex-only
# (той самий try/except, що вже є). Тобто найгірший випадок з цим кроком
# — такий самий, як якби кроку не було: чистий regex, без падіння сервісу.
echo "🧠 Pre-warming PREEMPTIVE_MONOPOLY_SEMANTIC (ONNX model download)..."
timeout 120 python3 -c "
import time
t0 = time.time()
try:
    from preemptive_monopoly_embeddings import score_preemptive_monopoly_semantic
    score_preemptive_monopoly_semantic('прогрів моделі перед стартом')
    print(f'✅ Semantic model pre-warmed in {round(time.time()-t0,1)}s')
except Exception as e:
    print(f'⚠️  Semantic pre-warm failed (non-fatal, will fall back to regex-only at runtime): {e}')
" || echo "⚠️  Semantic pre-warm timed out after 120s (non-fatal, will fall back to regex-only at runtime)"
echo ""

echo "🔄 Starting Gunicorn..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Start gunicorn
exec gunicorn app:app
