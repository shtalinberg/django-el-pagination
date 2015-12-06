"""Decorator tests."""

from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory

from el_pagination import decorators


class DecoratorsTestMixin(object):
    """Base test mixin for decorators.

    Subclasses (actual test cases) must implement the ``get_decorator`` method
    and the ``arg`` attribute to be used as argument for the decorator.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.ajax_headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        self.default = 'default.html'
        self.page = 'page.html'
        self.page_url = '/?page=2&mypage=10&querystring_key=page'
        self.mypage = 'mypage.html'
        self.mypage_url = '/?page=2&mypage=10&querystring_key=mypage'

    def get_decorator(self):
        """Return the decorator that must be exercised."""
        raise NotImplementedError

    def assertTemplatesEqual(self, expected_active, expected_page, templates):
        """Assert active template and page template are the ones given."""
        self.assertSequenceEqual([expected_active, expected_page], templates)

    def decorate(self, *args, **kwargs):
        """Return a view decorated with ``self.decorator(*args, **kwargs)``."""

        def view(request, extra_context=None, template=self.default):
            """Test view that will be decorated in tests."""
            context = {}
            if extra_context is not None:
                context.update(extra_context)
            return template, context['page_template']

        decorator = self.get_decorator()
        return decorator(*args, **kwargs)(view)

    def test_decorated(self):
        # Ensure the view is correctly decorated.
        view = self.decorate(self.arg)
        templates = view(self.factory.get('/'))
        self.assertTemplatesEqual(self.default, self.page, templates)

    def test_request_with_querystring_key(self):
        # If the querystring key refers to the handled template,
        # the view still uses the default tempate if the request is not Ajax.
        view = self.decorate(self.arg)
        templates = view(self.factory.get(self.page_url))
        self.assertTemplatesEqual(self.default, self.page, templates)

    def test_ajax_request(self):
        # Ensure the view serves the template fragment if the request is Ajax.
        view = self.decorate(self.arg)
        templates = view(self.factory.get('/', **self.ajax_headers))
        self.assertTemplatesEqual(self.page, self.page, templates)

    def test_ajax_request_with_querystring_key(self):
        # If the querystring key refers to the handled template,
        # the view switches the template if the request is Ajax.
        view = self.decorate(self.arg)
        templates = view(self.factory.get(self.page_url, **self.ajax_headers))
        self.assertTemplatesEqual(self.page, self.page, templates)

    def test_unexistent_page(self):
        # Ensure the default page and is returned if the querystring points
        # to a page that is not defined.
        view = self.decorate(self.arg)
        templates = view(self.factory.get('/?querystring_key=does-not-exist'))
        self.assertTemplatesEqual(self.default, self.page, templates)


class PageTemplateTest(DecoratorsTestMixin, TestCase):

    arg = 'page.html'

    def get_decorator(self):
        return decorators.page_template

    def test_request_with_querystring_key_to_mypage(self):
        # If the querystring key refers to another template,
        # the view still uses the default tempate if the request is not Ajax.
        view = self.decorate(self.arg)
        templates = view(self.factory.get(self.mypage_url))
        self.assertTemplatesEqual(self.default, self.page, templates)

    def test_ajax_request_with_querystring_key_to_mypage(self):
        # If the querystring key refers to another template,
        # the view still uses the default tempate even if the request is Ajax.
        view = self.decorate(self.arg)
        templates = view(
            self.factory.get(self.mypage_url, **self.ajax_headers))
        self.assertTemplatesEqual(self.default, self.page, templates)

    def test_ajax_request_to_mypage(self):
        # Ensure the view serves the template fragment if the request is Ajax
        # and another template fragment is requested.
        view = self.decorate(self.mypage, key='mypage')
        templates = view(
            self.factory.get(self.mypage_url, **self.ajax_headers))
        self.assertTemplatesEqual(self.mypage, self.mypage, templates)


class PageTemplatesTest(DecoratorsTestMixin, TestCase):

    arg = {'page.html': None, 'mypage.html': 'mypage'}

    def get_decorator(self):
        return decorators.page_templates

    def test_request_with_querystring_key_to_mypage(self):
        # If the querystring key refers to another template,
        # the view still uses the default tempate if the request is not Ajax.
        view = self.decorate(self.arg)
        templates = view(self.factory.get(self.mypage_url))
        self.assertTemplatesEqual(self.default, self.mypage, templates)

    def test_ajax_request_with_querystring_key_to_mypage(self):
        # If the querystring key refers to another template,
        # the view switches to the givent template if the request is Ajax.
        view = self.decorate(self.arg)
        templates = view(
            self.factory.get(self.mypage_url, **self.ajax_headers))
        self.assertTemplatesEqual(self.mypage, self.mypage, templates)


class PageTemplatesWithTupleTest(PageTemplatesTest):

    arg = (('page.html', None), ('mypage.html', 'mypage'))
