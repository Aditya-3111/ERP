"""FinLedger Pro - Django project package.

Importing this package (it happens before settings are read) does two things:

1. loads ``backend/.env``;
2. if MySQL is the database, lets Django talk to MySQL through *PyMySQL*
   (pure Python - nothing to compile on Windows).
"""
from .env import get, load_env

load_env()

if get('DB_ENGINE', 'mysql').lower() == 'mysql':
    try:
        import pymysql
    except ImportError as exc:  # pragma: no cover - only when packages are missing
        raise ImportError(
            "PyMySQL is not installed. Activate the virtual environment and run:\n"
            "    pip install -r requirements.txt"
        ) from exc
    # Django 5 insists on mysqlclient >= 2.2.1; PyMySQL speaks the same API.
    pymysql.version_info = (2, 2, 1, 'final', 0)
    pymysql.install_as_MySQLdb()
