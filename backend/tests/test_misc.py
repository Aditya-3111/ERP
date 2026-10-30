"""Smaller endpoints."""

from tests.base import BaseAPITest


class MiscRouteTests(BaseAPITest):
    def test_low_stock_endpoint_no_longer_500(self):
        self.assertEqual(self.client.get('/api/inventory/items/low_stock/').status_code, 200)

    def test_asset_categories_alias(self):
        self.assertEqual(self.client.get('/api/maintenance/asset-categories/').status_code, 200)
        self.assertEqual(self.client.get('/api/maintenance/categories/').status_code, 200)


class PaginationTests(BaseAPITest):
    def test_page_size_parameter_is_honoured(self):
        from apps.hr.models import Department
        for i in range(25):
            Department.objects.create(name=f'D{i:02d}')
        self.assertEqual(len(self.client.get('/api/hr/departments/').json()['results']), 20)
        self.assertEqual(len(self.client.get('/api/hr/departments/?page_size=100').json()['results']), 25)


class FriendlyErrorTests(BaseAPITest):
    def test_duplicate_unique_value_is_400_not_500(self):
        body = {'user': str(self.user.guid), 'theme_name': 'dark'}
        first = self.client.post('/api/admin/themes/', body, format='json')
        self.assertEqual(first.status_code, 201, first.content)
        second = self.client.post('/api/admin/themes/', body, format='json')
        self.assertEqual(second.status_code, 400)          # a clear message, never a crash
