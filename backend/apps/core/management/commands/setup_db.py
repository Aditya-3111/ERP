"""python manage.py setup_db

Creates the MySQL database (if missing), all tables, the starting data and -
if SEED_DEMO_DATA=true in .env - sample records.  Safe to run many times.

    python manage.py setup_db              # normal
    python manage.py setup_db --no-demo    # without sample records
    python manage.py setup_db --reset --yes  # DROP the database and build it again
"""
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.core import db_bootstrap


class Command(BaseCommand):
    help = 'Create the database, tables and starting data automatically.'

    def add_arguments(self, parser):
        parser.add_argument('--no-demo', action='store_true', help='skip sample records')
        parser.add_argument('--demo', action='store_true', help='force sample records')
        parser.add_argument('--reset', action='store_true', help='DROP the database first (needs --yes)')
        parser.add_argument('--yes', action='store_true', help='confirm --reset')

    def handle(self, *args, **opts):
        if opts['reset']:
            if not opts['yes']:
                raise CommandError('--reset deletes ALL data. Add --yes if you are sure.')
            self._drop_database()

        demo = None
        if opts['no_demo']:
            demo = False
        elif opts['demo']:
            demo = True
        db_bootstrap.bootstrap(stdout=self.stdout, demo=demo)
        self.stdout.write(self.style.SUCCESS(
            f"Ready.  Login: {settings.ADMIN_USERNAME} / {settings.ADMIN_PASSWORD}"))

    def _drop_database(self):
        cfg = settings.DATABASES['default']
        name = cfg['NAME']
        if cfg['ENGINE'].endswith('sqlite3'):
            import os
            if os.path.exists(name):
                os.remove(name)
            self.stdout.write(f'Deleted sqlite file {name}')
            return
        if not db_bootstrap.database_name_is_safe(name):
            raise CommandError('unsafe DB_NAME')
        import pymysql
        conn = pymysql.connect(host=cfg['HOST'], port=int(cfg['PORT'] or 3306),
                               user=cfg['USER'], password=cfg['PASSWORD'])
        try:
            with conn.cursor() as cur:
                cur.execute(f'DROP DATABASE IF EXISTS `{name}`')
            conn.commit()
        finally:
            conn.close()
        self.stdout.write(f"Dropped database '{name}'")
