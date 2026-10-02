from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from core import middleware
from core.middleware import CurrentUserMiddleware, get_current_user
from core.templatetags.table_tags import sort_icon_class, sort_url
from brands.models import Brand


class CurrentUserMiddlewareTest(TestCase):
    def setUp(self):
        middleware._user.value = None

    def tearDown(self):
        middleware._user.value = None

    def test_get_current_user_returns_none_without_request(self):
        self.assertIsNone(get_current_user())

    def test_middleware_stores_request_user_during_request(self):
        user = User.objects.create_user(username='ana', password='senha123')
        request = RequestFactory().get('/')
        request.user = user

        captured = {}

        def get_response(req):
            captured['user'] = get_current_user()
            return req

        CurrentUserMiddleware(get_response)(request)

        self.assertEqual(captured['user'], user)
        self.assertIsNone(get_current_user())


class BaseModelAuditTest(TestCase):
    def setUp(self):
        middleware._user.value = None

    def tearDown(self):
        middleware._user.value = None

    def test_audit_fields_are_filled_from_current_user(self):
        user = User.objects.create_user(username='auditor', password='senha123')
        request = RequestFactory().get('/')
        request.user = user
        created = {}

        def get_response(req):
            created['brand'] = Brand.objects.create(name='Toyota')
            return req

        CurrentUserMiddleware(get_response)(request)

        self.assertEqual(created['brand'].user_created, user)
        self.assertEqual(created['brand'].user_updated, user)

    def test_audit_fields_stay_empty_without_user(self):
        brand = Brand.objects.create(name='Fiat')

        self.assertIsNone(brand.user_created)
        self.assertIsNone(brand.user_updated)


class TableTagsTest(TestCase):
    def _context(self, query):
        request = RequestFactory().get(f'/{query}')
        from django.template import Context
        return Context({'request': request})

    def test_sort_url_sets_ascending_order(self):
        self.assertEqual(sort_url(self._context(''), 'name'), '?order_by=name')

    def test_sort_url_toggles_to_descending(self):
        self.assertEqual(sort_url(self._context('?order_by=name'), 'name'), '?order_by=-name')

    def test_sort_url_toggles_back_to_ascending(self):
        self.assertEqual(sort_url(self._context('?order_by=-name'), 'name'), '?order_by=name')

    def test_sort_icon_class_ascending(self):
        self.assertEqual(sort_icon_class(self._context('?order_by=name'), 'name'), 'bi-arrow-up')

    def test_sort_icon_class_descending(self):
        self.assertEqual(sort_icon_class(self._context('?order_by=-name'), 'name'), 'bi-arrow-down')

    def test_sort_icon_class_neutral(self):
        self.assertEqual(sort_icon_class(self._context(''), 'name'), 'bi-arrow-down-up')
