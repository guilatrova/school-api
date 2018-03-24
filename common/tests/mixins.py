from django.urls import reverse, resolve
from rest_framework import status

class UrlTestMixin:
    allowed_single = ['get', 'put', 'delete']
    allowed_list = ['get', 'post']

    def test_resolves_list_url(self):
        resolver = self.resolve_by_name(self.list_name)
        self.assertEqual(resolver.func.cls, self.view)

    def test_resolves_single_url(self):
        resolver = self.resolve_by_name(self.single_name, pk=1)
        self.assertEqual(resolver.func.cls, self.view)

    def test_list_url_allows(self):
        resolver = self.resolve_by_name(self.list_name)
        self.assert_has_actions(self.allowed_list, resolver.func.actions)

    def test_single_url_allows(self):
        resolver = self.resolve_by_name(self.single_name, pk=1)
        self.assert_has_actions(self.allowed_single, resolver.func.actions)

    def resolve_by_name(self, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)

    def assert_has_actions(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for action in expected:
            self.assertIn(action, actual)

class ApiTestMixin:
    def test_creates(self):
        response = self.client.post(self.list_url, self.post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.count(), 2)

    def test_lists(self):
        response = self.client.get(self.list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update(self):
        data = self.update_data

        response = self.client.put(self.single_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pre_created_entity.refresh_from_db()
        self.assertEqual(self.pre_created_entity.name, data['name'])

    def test_retrieves(self):
        response = self.client.get(self.single_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.pre_created_entity.name)

    def test_deletes(self):
        response = self.client.delete(self.single_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.model.objects.count(), 0)