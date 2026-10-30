"""Create the database, the tables and the starting data - automatically.

Used by  ``python manage.py setup_db``  and by  ``python manage.py runserver``.
Nothing here is specific to one module, so it lives in the core app.
"""
import re

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError

_SAFE_NAME = re.compile(r'^[A-Za-z0-9_]+$')


def _db():
    return settings.DATABASES['default']


def database_name_is_safe(name):
    """Only letters, digits and underscore - the name is put into SQL text."""
    return bool(name) and bool(_SAFE_NAME.match(name))


def ensure_database(stdout=None):
    """MySQL: run CREATE DATABASE IF NOT EXISTS.  SQLite: nothing to do.

    Returns True when the database had to be created, False if it existed.
    """
    cfg = _db()
    if not cfg['ENGINE'].endswith('mysql'):
        return False

    name = cfg['NAME']
    if not database_name_is_safe(name):
        raise CommandError(f"DB_NAME '{name}' is not allowed - use only letters, digits and _")

    import pymysql  # installed through requirements.txt

    try:
        conn = pymysql.connect(
            host=cfg['HOST'], port=int(cfg['PORT'] or 3306),
            user=cfg['USER'], password=cfg['PASSWORD'],
            charset='utf8mb4', connect_timeout=8,
        )
    except pymysql.err.OperationalError as exc:
        code = exc.args[0] if exc.args else 0
        if code == 1045:
            raise CommandError(
                f"MySQL refused the login for user '{cfg['USER']}'.\n"
                "-> Open backend/.env and correct DB_USER / DB_PASSWORD."
            ) from exc
        raise CommandError(
            f"Could not connect to MySQL at {cfg['HOST']}:{cfg['PORT']}.\n"
            "-> Start the MySQL service (XAMPP: press Start next to MySQL), "
            "then check DB_HOST / DB_PORT in backend/.env.\n"
            f"   ({exc})"
        ) from exc

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM information_schema.schemata WHERE schema_name = %s", (name,))
            existed = cur.fetchone()[0] > 0
            if not existed:
                cur.execute(
                    f"CREATE DATABASE `{name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
        conn.commit()
    finally:
        conn.close()

    if stdout and not existed:
        stdout.write(f"Created database '{name}'.")
    return not existed


def bootstrap(stdout=None, demo=None, seed=True):
    """database -> tables (migrate) -> masters -> optional demo data."""
    say = stdout.write if stdout else (lambda *_: None)
    created = ensure_database(stdout)
    if not created and _db()['ENGINE'].endswith('mysql'):
        say(f"Database '{_db()['NAME']}' already exists.")

    say('Creating / updating tables ...')
    call_command('migrate', interactive=False, verbosity=0)

    if seed:
        say('Adding starting data (roles, account groups, voucher types, admin user) ...')
        call_command('seed_masters', verbosity=0)
        if demo is None:
            demo = settings.SEED_DEMO_DATA
        if demo:
            _load_demo_once()
    return created


def _load_demo_once():
    """Sample records are inserted ONE time only. Without this marker they would come back
    every time the server starts, even after you deleted them."""
    from apps.core.models import SystemSetting
    marker, created = SystemSetting.objects.get_or_create(
        key='demo_data_loaded', defaults={'value': 'yes', 'setting_type': 'text',
                                          'description': 'Sample records were inserted (do not delete)'})
    if created:
        call_command('seed_demo', verbosity=0)
