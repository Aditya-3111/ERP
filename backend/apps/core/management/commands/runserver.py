"""python manage.py runserver  - same as Django's, but first makes sure the
database, the tables and the starting data exist (so a new computer needs no
manual SQL).  Turn it off with AUTO_SETUP_DB=false in .env.
"""
import os

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as StaticRunserver

from apps.core import db_bootstrap


class Command(StaticRunserver):
    def handle(self, *args, **options):
        # The auto-reloader starts this command twice (parent + child); set up only once.
        if settings.AUTO_SETUP_DB and os.environ.get('RUN_MAIN') != 'true':
            self.stdout.write(self.style.MIGRATE_HEADING('Preparing database ...'))
            db_bootstrap.bootstrap(stdout=self.stdout)
            self.stdout.write(self.style.SUCCESS('Database is ready.\n'))
        return super().handle(*args, **options)
