# gunicorn.conf.py — Veritas Protocol (Render free tier)
# gunicorn сам підхоплює цей файл із поточної теки. УВАГА: прапорці в Start Command
# (--timeout, -k/--worker-class, -w, --bind) мають ПРІОРИТЕТ над цим файлом —
# прибери їх зі Start Command (достатньо: `gunicorn app:app -c gunicorn.conf.py`).
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# gthread: heartbeat воркера йде з головного потоку, а запити — у потоках. Довгий
# запит (Haiku чекає 10-30с) більше не виглядає як «завислий воркер».
# 1 процес — бо RAM на free-tier обмежена; паралельність дають потоки.
worker_class = 'gthread'
workers = int(os.environ.get('WEB_CONCURRENCY', '1'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))

# Має бути СУТТЄВО більшим за ANTHROPIC_TIMEOUT_S (див. app.py: дефолт 55с).
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
graceful_timeout = 30
keepalive = 5

# heartbeat-файл у RAM (без блокувань від диска) — рекомендація gunicorn для контейнерів
worker_tmp_dir = '/dev/shm' if os.path.isdir('/dev/shm') else None

accesslog = '-'
errorlog = '-'
loglevel = 'info'


def post_fork(server, worker):
    # app.py читає це при імпорті (до fork воно ще не відоме) і звіряє
    # ANTHROPIC_TIMEOUT_S з реальним timeout — див. «TIMEOUT MISCONFIG» у логах.
    os.environ['GUNICORN_EFFECTIVE_TIMEOUT'] = str(server.cfg.timeout)


def worker_abort(worker):
    # Викликається на SIGABRT (зазвичай = WORKER TIMEOUT). До SIGKILL лишається ~1с:
    # best-effort позначаємо запити, що були в польоті, як killed у request_log.
    # Запасний варіант, якщо не встигли: view request_log_v (started >4 хв -> killed).
    try:
        import sys
        mod = sys.modules.get('request_log')
        if mod is not None:
            mod.mark_inflight_killed('gunicorn_worker_abort')
    except Exception:
        pass
