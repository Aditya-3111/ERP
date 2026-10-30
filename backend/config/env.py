"""Tiny .env loader (no third-party package needed).

Reads ``backend/.env`` once and puts every KEY=VALUE into ``os.environ``.
A variable that is already set in the real environment always wins, so you can
override anything from the terminal, e.g.  ``set DB_NAME=other`` (Windows).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
_loaded = False


def load_env(path=None):
    global _loaded
    if _loaded:
        return
    _loaded = True
    env_file = Path(path) if path else BASE_DIR / '.env'
    if not env_file.exists():
        return
    for raw in env_file.read_text(encoding='utf-8-sig').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        key, value = key.strip(), value.strip()
        # allow:  KEY="value with spaces"   KEY='value'   KEY=value  # comment
        if value[:1] in ('"', "'") and value[-1:] == value[:1] and len(value) >= 2:
            value = value[1:-1]
        else:
            value = value.split(' #', 1)[0].strip()
        os.environ.setdefault(key, value)


def get(name, default=None):
    load_env()
    return os.environ.get(name, default)


def get_bool(name, default=False):
    value = get(name)
    if value is None:
        return default
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')


def get_list(name, default=''):
    return [x.strip() for x in str(get(name, default)).split(',') if x.strip()]
