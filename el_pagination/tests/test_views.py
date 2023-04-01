"""View tests."""



from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory

from el_pagination import views
from project.models import TestModel, make_model_instances


class AjaxListViewTest(TestCase):

    model_page_template = 'el_pagination/testmodel_list_page.html'
    model_template_name = 'el_pagination/testmodel_list.html'
    page_template = 'page_template.html'
    template_name = 'template.html'
    url = '/?page=2'

    def setUp(self):
        factory = RequestFactory()
        self.request = factory.get(self.url)
        self.ajax_request = factory.get(
            self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def check_response(self, response, template_name, object_list):
        """Execute several assertions on the response.

        Check that the response has a successful status code,
        uses ``template_name`` and contains ``object_list``.
        """
        self.assertEqual(200, response.status_code)
        self.assertSequenceEqual([template_name], response.template_name)
        self.assertSequenceEqual(
            list(object_list), response.context_data['object_list'])

    def make_view(self, *args, **kwargs):
        """Return an instance of AjaxListView."""
        return views.AjaxListView.as_view(*args, **kwargs)

    def test_list(self):
        # Ensure the view correctly adds the list to context.
        view = self.make_view(
            queryset=range(30),
            template_name=self.template_name,
            page_template=self.page_template,
        )
        response = view(self.request)
        self.check_response(response, self.template_name, range(30))

    def test_list_ajax(self):
        # Ensure the list view switches templates when the request is Ajax.
        view = self.make_view(
            queryset=range(30),
            template_name=self.template_name,
            page_template=self.page_template,
        )
        response = view(self.ajax_request)
        self.check_response(response, self.page_template, range(30))

    def test_queryset(self):
        # Ensure the view correctly adds the queryset to context.
        queryset = make_model_instances(30)
        view = self.make_view(queryset=queryset)
        response = view(self.request)
        self.check_response(response, self.model_template_name, queryset)

    def test_queryset_ajax(self):
        # Ensure the queryset view switches templates when the request is Ajax.
        queryset = make_model_instances(30)
        view = self.make_view(queryset=queryset)
        response = view(self.ajax_request)
        self.check_response(response, self.model_page_template, queryset)

    def test_model(self):
        # Ensure the view correctly uses the model to generate the template.
        queryset = make_model_instances(30)
        view = self.make_view(model=TestModel)
        response = view(self.request)
        self.check_response(response, self.model_template_name, queryset)

    def test_model_ajax(self):
        # Ensure the model view switches templates when the request is Ajax.
        queryset = make_model_instances(30)
        view = self.make_view(model=TestModel)
        response = view(self.ajax_request)
        self.check_response(response, self.model_page_template, queryset)

    def test_missing_queryset_or_model(self):
        # An error is raised if both queryset and model are not provided.
        view = self.make_view()
        with self.assertRaises(ImproperlyConfigured) as cm:
            view(self.request)
        self.assertIn('queryset', str(cm.exception))
        self.assertIn('model', str(cm.exception))

    def test_missing_page_template(self):
        # An error is raised if the ``page_template`` name is not provided.
        view = self.make_view(queryset=range(30))
        with self.assertRaises(ImproperlyConfigured) as cm:
            view(self.request)
        self.assertIn('page_template', str(cm.exception))

    def test_do_not_allow_empty(self):
        # An error is raised if the list is empty and ``allow_empty`` is
        # set to False.
        view = self.make_view(model=TestModel, allow_empty=False)
        with self.assertRaises(Http404) as cm:
            view(self.request)
        self.assertIn('allow_empty', str(cm.exception))

    def test_view_in_context(self):
        # Ensure the view is included in the template context.
        view = self.make_view(
            queryset=range(30),
            page_template=self.page_template,
        )
        response = view(self.ajax_request)
        view_instance = response.context_data['view']
        self.assertIsInstance(view_instance, views.AjaxListView)
