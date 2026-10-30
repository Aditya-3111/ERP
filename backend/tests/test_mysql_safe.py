"""Catches SQL that works on SQLite but is REJECTED by MySQL / MariaDB.

MySQL error 1235: "doesn't yet support 'LIMIT & IN/ALL/ANY/SOME subquery'" - e.g.
    Entry.objects.filter(voucher__in=Voucher.objects.all()[:6])
Fix: turn the sliced queryset into a list first.  This test reads the SQL of every list
page, report and the dashboard and fails if such a query appears.
"""
import re
import uuid

from django.core.management import call_command
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import get_resolver

from tests.base import BaseAPITest

LIMIT_IN_SUBQUERY = re.compile(r'\bIN\s*\(\s*SELECT\b.*?\bLIMIT\b', re.I | re.S)


def list_urls():
    urls = []

    def walk(patterns, prefix=''):
        for p in patterns:
            text = (prefix + str(p.pattern)).replace('^', '').replace('$', '')
            if hasattr(p, 'url_patterns'):
                walk(p.url_patterns, text)
            elif text.startswith('api/') and '<' not in text and '(?P' not in text and 'format' not in text:
                urls.append('/' + text)
    walk(get_resolver().url_patterns)
    return sorted(set(urls))


class MySqlSafeSqlTests(BaseAPITest):
    def test_no_limit_inside_in_subquery(self):
        call_command('seed_masters', verbosity=0)
        call_command('seed_demo', verbosity=0)
        bad = []
        for url in list_urls():
            if url.endswith(('/logout/', '/refresh/', '/login/', '/change-password/')):
                continue
            with CaptureQueriesContext(connection) as ctx:
                self.client.get(url, {'from': '2026-04-01', 'to': '2027-03-31'})
            for q in ctx.captured_queries:
                if LIMIT_IN_SUBQUERY.search(q['sql']):
                    bad.append(f"{url}: {q['sql'][:160]}")
        self.assertEqual(bad, [], '\n' + '\n'.join(bad))

    def test_detector_really_detects(self):
        # Only BUILD the bad query and read its SQL text - never run it (MySQL would raise error 1235).
        from apps.finance.models import AccountingEntry, Voucher
        bad_query = AccountingEntry.objects.filter(voucher__in=Voucher.objects.all()[:6])
        self.assertTrue(LIMIT_IN_SUBQUERY.search(str(bad_query.query)))
        good_query = AccountingEntry.objects.filter(voucher__in=[uuid.uuid4()])      # a plain list is fine
        self.assertFalse(LIMIT_IN_SUBQUERY.search(str(good_query.query)))