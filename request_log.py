"""
request_log.py — журнал КОЖНОГО POST /api/* запиту (Supabase, таблиця request_log).

Навіщо: witness_log/trigger_log пишуться лише ПІСЛЯ успіху. Якщо gunicorn вбиває
воркер (WORKER TIMEOUT -> SIGKILL) посеред виклику Haiku, жоден except не
спрацьовує, нічого не пишеться, а Anthropic токени вже порахував. Тут рядок
створюється НА ПОЧАТКУ запиту (status='started') і закривається в кінці.
Рядок, що залишився в 'started' — це вбитий/загублений запит.

Підключення (app.py): request_log.init(app, _get_sb, APP_VERSION)
Точкові ноти з ендпоінтів: note(), note_llm(), note_error(), phase().

Принципи:
  - логування НІКОЛИ не ламає запит і не додає затримки: усі записи йдуть через
    одну фонову нитку (FIFO, тож INSERT завжди раніше за UPDATE);
  - вимкнути: змінна середовища REQUEST_LOG=0.
"""
import os
import time
import uuid
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor

from flask import g, request, got_request_exception

_ENABLED = os.environ.get('REQUEST_LOG', '1') != '0'
_TABLE = 'request_log'
_SKIP_PREFIXES = ('/api/stats', '/api/health')
_COLUMNS = {'model', 'anthropic_request_id', 'stop_reason', 'input_tokens', 'output_tokens',
            'llm_latency_ms', 'status', 'raw_text', 'error_type', 'error_msg', 'hint', 'phase'}
_RAW_CAP = 20000          # символів сирої відповіді LLM (лише при невдачі)
_ERR_CAP = 500

_get_sb = None
_app_version = ''
_pool = None
_INFLIGHT = {}            # rid -> t0; потрібно для hook'а worker_abort
_lock = threading.Lock()


def _kind_from_path(path: str) -> str:
    p = path[len('/api/'):] if path.startswith('/api/') else path.lstrip('/')
    return (p or 'root')[:80]


def _submit(fn):
    """Усі записи в БД — через одну нитку: порядок збережено, запит не блокується."""
    if _pool is None:
        return

    def _run():
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            print(f"⚠️  request_log write failed (non-fatal): {type(e).__name__}: {str(e)[:200]}")
    try:
        _pool.submit(_run)
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  request_log submit failed (non-fatal): {e}")


def _insert(row):
    sb = _get_sb()
    if sb:
        sb.table(_TABLE).insert(row).execute()


def _update(rid, fields):
    sb = _get_sb()
    if sb:
        sb.table(_TABLE).update(fields).eq('id', rid).execute()


def _now_iso():
    return time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()) + 'Z'


# ── API для ендпоінтів ─────────────────────────────────────────────────────
def note(**fields):
    """Додати поля до рядка поточного запиту (записується в кінці запиту)."""
    rl = getattr(g, 'rl', None)
    if rl is not None:
        rl['notes'].update({k: v for k, v in fields.items() if v is not None and k in _COLUMNS})


def phase(name: str):
    """Одразу (не чекаючи кінця запиту) оновити phase — напр. 'llm' перед викликом Haiku.
    Якщо воркер помре під час виклику, рядок покаже, на якій фазі це сталось."""
    rl = getattr(g, 'rl', None)
    if rl is None:
        return
    rl['notes']['phase'] = name
    rid = rl['id']
    _submit(lambda: _update(rid, {'phase': name, 'updated_at': _now_iso()}))


def note_llm(msg, t0: float, raw: str = '', model: str = None):
    """Зафіксувати результат виклику Anthropic. Не кидає винятків."""
    try:
        usage = getattr(msg, 'usage', None)
        stop = getattr(msg, 'stop_reason', None)
        fields = dict(
            anthropic_request_id=getattr(msg, '_request_id', None),
            stop_reason=stop,
            input_tokens=getattr(usage, 'input_tokens', None),
            output_tokens=getattr(usage, 'output_tokens', None),
            llm_latency_ms=int((time.time() - t0) * 1000),
            model=model or getattr(msg, 'model', None),
        )
        if stop == 'max_tokens':
            fields['status'] = 'truncated'
            fields['raw_text'] = (raw or '')[:_RAW_CAP]
        note(**fields)
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  request_log.note_llm error (non-fatal): {e}")


def note_error(exc: BaseException):
    try:
        note(error_type=type(exc).__name__, error_msg=str(exc)[:_ERR_CAP])
    except Exception:  # noqa: BLE001
        pass


def mark_inflight_killed(reason: str = 'worker_abort'):
    """Для gunicorn worker_abort: синхронно позначити всі запити цього воркера як killed.
    Є ~1 с до SIGKILL, тому один пакетний UPDATE; best-effort."""
    if not _ENABLED or _get_sb is None:
        return
    with _lock:
        ids = list(_INFLIGHT.keys())
    if not ids:
        return
    try:
        sb = _get_sb()
        if sb:
            (sb.table(_TABLE)
               .update({'status': 'killed', 'error_type': reason, 'updated_at': _now_iso()})
               .in_('id', ids).eq('status', 'started').execute())
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  request_log.mark_inflight_killed failed: {e}")


# ── hooks ──────────────────────────────────────────────────────────────────
def _before():
    if not _ENABLED or request.method != 'POST':
        return
    path = request.path
    if not path.startswith('/api/') or path.startswith(_SKIP_PREFIXES):
        return
    try:
        j = request.get_json(silent=True)   # Flask кешує — ендпоінти прочитають те саме
        if not isinstance(j, dict):
            j = {}
        text = j.get('article_text') or j.get('text') or j.get('text_preview') or ''
        norm = ' '.join(str(text).split())
        rid = str(uuid.uuid4())
        t0 = time.time()
        row = {
            'id': rid,
            'kind': _kind_from_path(path),
            'status': 'started',
            'phase': 'start',
            'app_version': _app_version,
            'worker_pid': os.getpid(),
            'text_sha256': hashlib.sha256(norm.encode('utf-8')).hexdigest() if norm else None,
            'input_chars': len(norm) if norm else None,
            'experiment_id': (str(j.get('experiment_id'))[:100] if j.get('experiment_id') else None),
            'variant': (str(j.get('variant'))[:100] if j.get('variant') else None),
            'url': (str(j.get('url'))[:500] if j.get('url') else None),
        }
        g.rl = {'id': rid, 't0': t0, 'notes': {}}
        with _lock:
            _INFLIGHT[rid] = t0
        _submit(lambda: _insert(row))
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  request_log before_request error (non-fatal): {e}")


def _status_from_http(code: int, hint: str) -> str:
    if code < 400:
        return 'ok'
    if code == 504 or hint in ('llm_timeout', 'analysis_timeout'):
        return 'timeout'
    if code == 503 and hint == 'analysis_busy':
        return 'busy'
    if 400 <= code < 500:
        return 'bad_request'
    return 'error'


def _after(response):
    rl = getattr(g, 'rl', None)
    if rl is None or rl.get('closed'):
        return response
    try:
        code = response.status_code
        hint = ''
        if code >= 400 and (response.content_length or 0) < 4096:
            body = response.get_json(silent=True)
            if isinstance(body, dict):
                hint = str(body.get('hint') or '')[:80]
                rl['notes'].setdefault('hint', hint or None)
                if body.get('error'):
                    rl['notes'].setdefault('error_msg', str(body['error'])[:_ERR_CAP])
        notes = dict(rl['notes'])
        fields = {
            'http_status': code,
            'latency_ms': int((time.time() - rl['t0']) * 1000),
            'phase': 'done',
            'updated_at': _now_iso(),
        }
        fields.update(notes)
        fields['phase'] = 'done'
        fields['status'] = notes.get('status') or _status_from_http(code, hint)
        rl['closed'] = True
        rid = rl['id']
        _submit(lambda: _update(rid, fields))
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  request_log after_request error (non-fatal): {e}")
    return response


def _teardown(exc):
    rl = getattr(g, 'rl', None)
    if rl is None:
        return
    with _lock:
        _INFLIGHT.pop(rl['id'], None)
    if exc is not None and not rl.get('closed'):
        rid = rl['id']
        fields = {'status': 'error', 'phase': 'done', 'updated_at': _now_iso(),
                  'latency_ms': int((time.time() - rl['t0']) * 1000),
                  'error_type': type(exc).__name__, 'error_msg': str(exc)[:_ERR_CAP]}
        _submit(lambda: _update(rid, fields))


def _on_exception(sender, exception, **extra):
    # іменована функція, не lambda: blinker тримає слабке посилання на receiver
    note_error(exception)


def init(app, get_sb, app_version: str):
    """Зареєструвати hooks. Викликати один раз, після створення app і _get_sb."""
    global _get_sb, _app_version, _pool
    if not _ENABLED:
        print("ℹ️  request_log disabled (REQUEST_LOG=0)")
        return
    _get_sb = get_sb
    _app_version = app_version
    _pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix='reqlog')
    app.before_request(_before)
    app.after_request(_after)
    app.teardown_request(_teardown)
    # необроблений виняток: Flask сам віддає 500 і after_request уже не знає причини
    got_request_exception.connect(_on_exception, app)
    print("✅ request_log enabled (before/after/teardown hooks)")
