from django.urls import reverse, resolve

class UrlTestMixin:
    def test_resolves_list_url(self):
        resolver = self.resolve_by_name(self.list_name)
        self.assertEqual(resolver.func.cls, self.view)

    def test_resolves_single_url(self):
        resolver = self.resolve_by_name(self.single_name, pk=1)
        self.assertEqual(resolver.func.cls, self.view)

    def test_list_url_allows(self):
        resolver = self.resolve_by_name(self.list_name)
        allowed = ['get', 'post']
        self.assert_has_actions(allowed, resolver.func.actions)

    def test_single_url_allows(self):
        resolver = self.resolve_by_name(self.single_name, pk=1)
        allowed = ['get', 'put', 'delete']
        self.assert_has_actions(allowed, resolver.func.actions)

    def resolve_by_name(self, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)

    def assert_has_actions(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for action in expected:
            self.assertIn(action, actual)