"""setup_db / seed commands, the .env reader and the MySQL bootstrap (with a fake MySQL)."""
import os
import sys
import tempfile
from types import SimpleNamespace
from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from apps.core import db_bootstrap
from apps.core.models import Role, User
from apps.finance.models import AccountGroup, VoucherType
from config import env as envmod


class SeedTests(TestCase):
    def test_masters_are_created_once(self):
        call_command('seed_masters', verbosity=0)
        counts = (Role.objects.count(), AccountGroup.objects.count(), VoucherType.objects.count(), User.objects.count())
        call_command('seed_masters', verbosity=0)          # second run must not duplicate anything
        self.assertEqual(counts, (Role.objects.count(), AccountGroup.objects.count(),
                                  VoucherType.objects.count(), User.objects.count()))
        self.assertTrue(User.objects.get(username='admin').check_password('admin'))
        self.assertTrue(AccountGroup.objects.filter(name='Sundry Debtors', primary_group='Current Assets').exists())

    def test_demo_data_idempotent_and_balanced(self):
        from django.db.models import Sum
        from apps.finance.models import AccountingEntry, Voucher
        call_command('seed_masters', verbosity=0)
        call_command('seed_demo', verbosity=0)
        n = Voucher.objects.count()
        call_command('seed_demo', verbosity=0)
        self.assertEqual(n, Voucher.objects.count())
        dr = AccountingEntry.objects.filter(is_dr=True).aggregate(t=Sum('amount'))['t']
        cr = AccountingEntry.objects.filter(is_dr=False).aggregate(t=Sum('amount'))['t']
        self.assertEqual(dr, cr)

    def test_setup_db_command_runs(self):
        call_command('setup_db', '--no-demo', verbosity=0)
        self.assertTrue(User.objects.filter(username='admin').exists())


class EnvFileTests(TestCase):
    def test_parser(self):
        with tempfile.NamedTemporaryFile('w', suffix='.env', delete=False, encoding='utf-8') as f:
            f.write('# comment\nFL_A=1\nFL_B="two words"\nFL_C=three # trailing\n\nFL_D=\n')
        envmod._loaded = False
        try:
            with mock.patch.dict(os.environ, {}, clear=False):
                envmod.load_env(f.name)
                self.assertEqual(os.environ['FL_A'], '1')
                self.assertEqual(os.environ['FL_B'], 'two words')
                self.assertEqual(os.environ['FL_C'], 'three')
                self.assertEqual(os.environ['FL_D'], '')
        finally:
            for k in ('FL_A', 'FL_B', 'FL_C', 'FL_D'):
                os.environ.pop(k, None)
            envmod._loaded = True
            os.unlink(f.name)


class FakeMySQL:
    """Stands in for PyMySQL so the CREATE DATABASE logic can be tested without a server."""

    class OperationalError(Exception):
        pass

    def __init__(self, db_exists=False, fail_with=None):
        self.executed = []
        self.db_exists = db_exists
        self.fail_with = fail_with
        self.err = SimpleNamespace(OperationalError=self.OperationalError)
        outer = self

        class Cursor:
            def __enter__(s): return s
            def __exit__(s, *a): return False
            def execute(s, sql, params=None): outer.executed.append((sql, params))
            def fetchone(s): return (1 if outer.db_exists else 0,)

        class Conn:
            def cursor(s): return Cursor()
            def commit(s): pass
            def close(s): outer.closed = True

        self._conn = Conn()

    def connect(self, **kw):
        self.connect_args = kw
        if self.fail_with:
            raise self.OperationalError(*self.fail_with)
        return self._conn


MYSQL_CFG = {'ENGINE': 'django.db.backends.mysql', 'NAME': 'fl_unit', 'USER': 'root',
             'PASSWORD': 'pw', 'HOST': '127.0.0.1', 'PORT': '3306'}


class BootstrapTests(TestCase):
    def run_ensure(self, fake, cfg=None):
        with mock.patch.dict(sys.modules, {'pymysql': fake}), \
                mock.patch.object(db_bootstrap, '_db', return_value=cfg or MYSQL_CFG):
            return db_bootstrap.ensure_database()

    def test_creates_missing_database_with_utf8mb4(self):
        fake = FakeMySQL(db_exists=False)
        self.assertTrue(self.run_ensure(fake))
        sql = [s for s, _ in fake.executed if s.startswith('CREATE')]
        self.assertEqual(len(sql), 1)
        self.assertIn('`fl_unit`', sql[0])
        self.assertIn('utf8mb4', sql[0])
        self.assertEqual(fake.connect_args['user'], 'root')
        self.assertEqual(fake.connect_args['password'], 'pw')
        self.assertNotIn('database', fake.connect_args)      # must connect WITHOUT a database

    def test_existing_database_is_left_alone(self):
        fake = FakeMySQL(db_exists=True)
        self.assertFalse(self.run_ensure(fake))
        self.assertFalse(any(s.startswith('CREATE') for s, _ in fake.executed))

    def test_unsafe_database_name_rejected(self):
        with self.assertRaises(CommandError):
            self.run_ensure(FakeMySQL(), dict(MYSQL_CFG, NAME='x`; DROP DATABASE y; --'))

    def test_wrong_password_gives_friendly_message(self):
        with self.assertRaises(CommandError) as ctx:
            self.run_ensure(FakeMySQL(fail_with=(1045, 'Access denied')))
        self.assertIn('.env', str(ctx.exception))
        self.assertIn('DB_PASSWORD', str(ctx.exception))

    def test_server_down_gives_friendly_message(self):
        with self.assertRaises(CommandError) as ctx:
            self.run_ensure(FakeMySQL(fail_with=(2003, "Can't connect")))
        self.assertIn('Start the MySQL service', str(ctx.exception))

    def test_sqlite_is_skipped(self):
        cfg = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}
        self.assertFalse(self.run_ensure(FakeMySQL(), cfg))


class DemoOnceTests(TestCase):
    def test_deleted_demo_records_do_not_come_back(self):
        from apps.crm.models import Customer
        db_bootstrap.bootstrap(demo=True)
        self.assertTrue(Customer.objects.filter(name='Sharma Traders').exists())
        Customer.objects.filter(name='Sharma Traders').delete()
        db_bootstrap.bootstrap(demo=True)                  # same as restarting the server
        self.assertFalse(Customer.objects.filter(name='Sharma Traders').exists())
