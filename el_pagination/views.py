"""Django EL Pagination class-based views."""


from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.encoding import smart_str
from django.utils.translation import gettext as _
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectTemplateResponseMixin

from el_pagination.settings import PAGE_LABEL


class MultipleObjectMixin(object):
    allow_empty = True
    context_object_name = None
    model = None
    queryset = None

    def get_queryset(self):
        """Get the list of items for this view.

        This must be an iterable, and may be a queryset
        (in which qs-specific behavior will be enabled).

        See original in ``django.views.generic.list.MultipleObjectMixin``.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            msg = '{0} must define ``queryset`` or ``model``'
            raise ImproperlyConfigured(msg.format(self.__class__.__name__))
        return queryset

    def get_allow_empty(self):
        """Returns True if the view should display empty lists.

        Return False if a 404 should be raised instead.

        See original in ``django.views.generic.list.MultipleObjectMixin``.
        """
        return self.allow_empty

    def get_context_object_name(self, object_list):
        """Get the name of the item to be used in the context.

        See original in ``django.views.generic.list.MultipleObjectMixin``.
        """
        if self.context_object_name:
            return self.context_object_name
        elif hasattr(object_list, 'model'):
            object_name = object_list.model._meta.object_name.lower()
            return smart_str(f'{object_name}_list')
        else:
            return None

    def get_context_data(self, **kwargs):
        """Get the context for this view.

        Also adds the *page_template* variable in the context.

        If the *page_template* is not given as a kwarg of the *as_view*
        method then it is generated using app label, model name
        (obviously if the list is a queryset), *self.template_name_suffix*
        and *self.page_template_suffix*.

        For instance, if the list is a queryset of *blog.Entry*,
        the template will be ``blog/entry_list_page.html``.
        """
        queryset = kwargs.pop('object_list')
        page_template = kwargs.pop('page_template')

        context_object_name = self.get_context_object_name(queryset)
        context = {'object_list': queryset, 'view': self}
        context.update(kwargs)
        if context_object_name is not None:
            context[context_object_name] = queryset

        if page_template is None:
            if hasattr(queryset, 'model'):
                page_template = self.get_page_template(**kwargs)
            else:
                raise ImproperlyConfigured('AjaxListView requires a page_template')
        context['page_template'] = self.page_template = page_template

        return context


class BaseListView(MultipleObjectMixin, View):
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            msg = _('Empty list and ``%(class_name)s.allow_empty`` is False.')
            raise Http404(msg % {'class_name': self.__class__.__name__})
        context = self.get_context_data(
            object_list=self.object_list, page_template=self.page_template
        )
        return self.render_to_response(context)


class InvalidPaginationListView:
    def get(self, request, *args, **kwargs):
        """Wraps super().get(...) in order to return 404 status code if
        the page parameter is invalid
        """
        response = super().get(request, args, kwargs)
        try:
            response.render()
        except Http404:
            request.GET = request.GET.copy()
            request.GET['page'] = '1'
            response = super().get(request, args, kwargs)
            response.status_code = 404

        return response


class AjaxMultipleObjectTemplateResponseMixin(MultipleObjectTemplateResponseMixin):
    key = PAGE_LABEL
    page_template = None
    page_template_suffix = '_page'
    template_name_suffix = '_list'

    def get_page_template(self, **kwargs):
        """Return the template name used for this request.

        Only called if *page_template* is not given as a kwarg of
        *self.as_view*.
        """
        opts = self.object_list.model._meta
        return '{0}/{1}{2}{3}.html'.format(
            opts.app_label,
            opts.object_name.lower(),
            self.template_name_suffix,
            self.page_template_suffix,
        )

    def get_template_names(self):
        """Switch the templates for Ajax requests."""
        request = self.request
        key = 'querystring_key'
        querystring_key = request.GET.get(key, request.POST.get(key, PAGE_LABEL))
        if (
            request.headers.get('x-requested-with') == 'XMLHttpRequest'
            and querystring_key == self.key
        ):
            return [self.page_template or self.get_page_template()]
        return super().get_template_names()


class AjaxListView(AjaxMultipleObjectTemplateResponseMixin, BaseListView):
    """Allows Ajax pagination of a list of objects.

    You can use this class-based view in place of *ListView* in order to
    recreate the behaviour of the *page_template* decorator.

    For instance, assume you have this code (taken from Django docs)::

        from django.conf.urls.defaults import *
        from django.views.generic import ListView

        from books.models import Publisher

        urlpatterns = patterns('',
            (r'^publishers/$', ListView.as_view(model=Publisher)),
        )

    You want to Ajax paginate publishers, so, as seen, you need to switch
    the template if the request is Ajax and put the page template
    into the context as a variable named *page_template*.

    This is straightforward, you only need to replace the view class, e.g.::

        from django.conf.urls.defaults import *

        from books.models import Publisher

        from el_pagination.views import AjaxListView

        urlpatterns = patterns('',
            (r'^publishers/$', AjaxListView.as_view(model=Publisher)),
        )

    NOTE: Django >= 1.3 is required to use this view.
    """
