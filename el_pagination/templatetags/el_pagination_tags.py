"""Django Endless Pagination template tags."""

from __future__ import unicode_literals
import re

from django import template
from django.utils.encoding import iri_to_uri
from django.http import Http404

from el_pagination import (
    models,
    settings,
    utils,
)
from el_pagination.paginators import (
    DefaultPaginator,
    EmptyPage,
    LazyPaginator,
)


PAGINATE_EXPRESSION = re.compile(r"""
    ^   # Beginning of line.
    (((?P<first_page>\w+)\,)?(?P<per_page>\w+)\s+)?  # First page, per page.
    (?P<objects>[\.\w]+)  # Objects / queryset.
    (\s+starting\s+from\s+page\s+(?P<number>[\-]?\d+|\w+))?  # Page start.
    (\s+using\s+(?P<key>[\"\'\-\w]+))?  # Querystring key.
    (\s+with\s+(?P<override_path>[\"\'\/\w]+))?  # Override path.
    (\s+as\s+(?P<var_name>\w+))?  # Context variable name.
    $   # End of line.
""", re.VERBOSE)
SHOW_CURRENT_NUMBER_EXPRESSION = re.compile(r"""
    ^   # Beginning of line.
    (starting\s+from\s+page\s+(?P<number>\w+))?\s*  # Page start.
    (using\s+(?P<key>[\"\'\-\w]+))?\s*  # Querystring key.
    (as\s+(?P<var_name>\w+))?  # Context variable name.
    $   # End of line.
""", re.VERBOSE)


register = template.Library()


@register.tag
def paginate(parser, token, paginator_class=None):
    """Paginate objects.

    Usage:

    .. code-block:: html+django

        {% paginate entries %}

    After this call, the *entries* variable in the template context is replaced
    by only the entries of the current page.

    You can also keep your *entries* original variable (usually a queryset)
    and add to the context another name that refers to entries of the current
    page, e.g.:

    .. code-block:: html+django

        {% paginate entries as page_entries %}

    The *as* argument is also useful when a nested context variable is provided
    as queryset. In this case, and only in this case, the resulting variable
    name is mandatory, e.g.:

    .. code-block:: html+django

        {% paginate entries.all as entries %}

    The number of paginated entries is taken from settings, but you can
    override the default locally, e.g.:

    .. code-block:: html+django

        {% paginate 20 entries %}

    Of course you can mix it all:

    .. code-block:: html+django

        {% paginate 20 entries as paginated_entries %}

    By default, the first page is displayed the first time you load the page,
    but you can change this, e.g.:

    .. code-block:: html+django

        {% paginate entries starting from page 3 %}

    When changing the default page, it is also possible to reference the last
    page (or the second last page, and so on) by using negative indexes, e.g:

    .. code-block:: html+django

        {% paginate entries starting from page -1 %}

    This can be also achieved using a template variable that was passed to the
    context, e.g.:

    .. code-block:: html+django

        {% paginate entries starting from page page_number %}

    If the passed page number does not exist, the first page is displayed.

    If you have multiple paginations in the same page, you can change the
    querydict key for the single pagination, e.g.:

    .. code-block:: html+django

        {% paginate entries using article_page %}

    In this case *article_page* is intended to be a context variable, but you
    can hardcode the key using quotes, e.g.:

    .. code-block:: html+django

        {% paginate entries using 'articles_at_page' %}

    Again, you can mix it all (the order of arguments is important):

    .. code-block:: html+django

        {% paginate 20 entries
            starting from page 3 using page_key as paginated_entries %}

    Additionally you can pass a path to be used for the pagination:

    .. code-block:: html+django

        {% paginate 20 entries
            using page_key with pagination_url as paginated_entries %}

    This way you can easily create views acting as API endpoints, and point
    your Ajax calls to that API. In this case *pagination_url* is considered a
    context variable, but it is also possible to hardcode the URL, e.g.:

    .. code-block:: html+django

        {% paginate 20 entries with "/mypage/" %}

    If you want the first page to contain a different number of items than
    subsequent pages, you can separate the two values with a comma, e.g. if
    you want 3 items on the first page and 10 on other pages:

    .. code-block:: html+django

    {% paginate 3,10 entries %}

    You must use this tag before calling the {% show_more %} one.
    """
    # Validate arguments.
    try:
        tag_name, tag_args = token.contents.split(None, 1)
    except ValueError:
        msg = '%r tag requires arguments' % token.contents.split()[0]
        raise template.TemplateSyntaxError(msg)

    # Use a regexp to catch args.
    match = PAGINATE_EXPRESSION.match(tag_args)
    if match is None:
        msg = 'Invalid arguments for %r tag' % tag_name
        raise template.TemplateSyntaxError(msg)

    # Retrieve objects.
    kwargs = match.groupdict()
    objects = kwargs.pop('objects')

    # The variable name must be present if a nested context variable is passed.
    if '.' in objects and kwargs['var_name'] is None:
        msg = (
            '%(tag)r tag requires a variable name `as` argumnent if the '
            'queryset is provided as a nested context variable (%(objects)s). '
            'You must either pass a direct queryset (e.g. taking advantage '
            'of the `with` template tag) or provide a new variable name to '
            'store the resulting queryset (e.g. `%(tag)s %(objects)s as '
            'objects`).'
        ) % {'tag': tag_name, 'objects': objects}
        raise template.TemplateSyntaxError(msg)

    # Call the node.
    return PaginateNode(paginator_class, objects, **kwargs)


@register.tag
def lazy_paginate(parser, token):
    """Lazy paginate objects.

    Paginate objects without hitting the database with a *select count* query.

    Use this the same way as *paginate* tag when you are not interested
    in the total number of pages.
    """
    return paginate(parser, token, paginator_class=LazyPaginator)


class PaginateNode(template.Node):
    """Add to context the objects of the current page.

    Also add the Django paginator's *page* object.
    """

    def __init__(
            self, paginator_class, objects, first_page=None, per_page=None,
            var_name=None, number=None, key=None, override_path=None):
        self.paginator = paginator_class or DefaultPaginator
        self.objects = template.Variable(objects)

        # If *var_name* is not passed, then the queryset name will be used.
        self.var_name = objects if var_name is None else var_name

        # If *per_page* is not passed then the default value form settings
        # will be used.
        self.per_page_variable = None
        if per_page is None:
            self.per_page = settings.PER_PAGE
        elif per_page.isdigit():
            self.per_page = int(per_page)
        else:
            self.per_page_variable = template.Variable(per_page)

        # Handle first page: if it is not passed then *per_page* is used.
        self.first_page_variable = None
        if first_page is None:
            self.first_page = None
        elif first_page.isdigit():
            self.first_page = int(first_page)
        else:
            self.first_page_variable = template.Variable(first_page)

        # Handle page number when it is not specified in querystring.
        self.page_number_variable = None
        if number is None:
            self.page_number = 1
        else:
            try:
                self.page_number = int(number)
            except ValueError:
                self.page_number_variable = template.Variable(number)

        # Set the querystring key attribute.
        self.querystring_key_variable = None
        if key is None:
            self.querystring_key = settings.PAGE_LABEL
        elif key[0] in ('"', "'") and key[-1] == key[0]:
            self.querystring_key = key[1:-1]
        else:
            self.querystring_key_variable = template.Variable(key)

        # Handle *override_path*.
        self.override_path_variable = None
        if override_path is None:
            self.override_path = None
        elif (
                override_path[0] in ('"', "'") and
                override_path[-1] == override_path[0]):
            self.override_path = override_path[1:-1]
        else:
            self.override_path_variable = template.Variable(override_path)

    def render(self, context):
        # Handle page number when it is not specified in querystring.
        if self.page_number_variable is None:
            default_number = self.page_number
        else:
            default_number = int(self.page_number_variable.resolve(context))

        # Calculate the number of items to show on each page.
        if self.per_page_variable is None:
            per_page = self.per_page
        else:
            per_page = int(self.per_page_variable.resolve(context))

        # Calculate the number of items to show in the first page.
        if self.first_page_variable is None:
            first_page = self.first_page or per_page
        else:
            first_page = int(self.first_page_variable.resolve(context))

        # User can override the querystring key to use in the template.
        # The default value is defined in the settings file.
        if self.querystring_key_variable is None:
            querystring_key = self.querystring_key
        else:
            querystring_key = self.querystring_key_variable.resolve(context)

        # Retrieve the override path if used.
        if self.override_path_variable is None:
            override_path = self.override_path
        else:
            override_path = self.override_path_variable.resolve(context)

        # Retrieve the queryset and create the paginator object.
        objects = self.objects.resolve(context)
        paginator = self.paginator(
            objects, per_page, first_page=first_page, orphans=settings.ORPHANS)

        # Normalize the default page number if a negative one is provided.
        if default_number < 0:
            default_number = utils.normalize_page_number(
                default_number, paginator.page_range)

        # The current request is used to get the requested page number.
        page_number = utils.get_page_number_from_request(
            context['request'], querystring_key, default=default_number)

        # Get the page.
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(1)
            if settings.PAGE_OUT_OF_RANGE_404:
                raise Http404('Page out of range')

        # Populate the context with required data.
        data = {
            'default_number': default_number,
            'override_path': override_path,
            'page': page,
            'querystring_key': querystring_key,
        }
        context.update({'endless': data, self.var_name: page.object_list})
        return ''


@register.inclusion_tag('el_pagination/show_more.html', takes_context=True)
def show_more(context, label=None, loading=settings.LOADING, class_name=None):
    """Show the link to get the next page in a Twitter-like pagination.

    Usage::

        {% show_more %}

    Alternatively you can override the label passed to the default template::

        {% show_more "even more" %}

    You can override the loading text too::

        {% show_more "even more" "working" %}

    You could pass in the extra CSS style class name as a third argument

       {% show_more "even more" "working" "class_name" %}

    Must be called after ``{% paginate objects %}``.
    """
    # This template tag could raise a PaginationError: you have to call
    # *paginate* or *lazy_paginate* before including the showmore template.
    data = utils.get_data_from_context(context)
    page = data['page']
    # show the template only if there is a next page
    if page.has_next():
        request = context['request']
        page_number = page.next_page_number()
        # Generate the querystring.
        querystring_key = data['querystring_key']
        querystring = utils.get_querystring_for_page(
            request, page_number, querystring_key,
            default_number=data['default_number'])
        return {
            'label': label,
            'loading': loading,
            'class_name': class_name,
            'path': iri_to_uri(data['override_path'] or request.path),
            'querystring': querystring,
            'querystring_key': querystring_key,
            'request': request,
        }
    # No next page, nothing to see.
    return {}


@register.tag
def get_pages(parser, token):
    """Add to context the list of page links.

    Usage:

    .. code-block:: html+django

        {% get_pages %}

    This is mostly used for Digg-style pagination.
    This call inserts in the template context a *pages* variable, as a sequence
    of page links. You can use *pages* in different ways:

    - just print *pages* and you will get Digg-style pagination displayed:

    .. code-block:: html+django

        {{ pages }}

    - display pages count:

    .. code-block:: html+django

        {{ pages|length }}

    - check if the page list contains more than one page:

    .. code-block:: html+django

        {{ pages.paginated }}
        {# the following is equivalent #}
        {{ pages|length > 1 }}

    - get a specific page:

    .. code-block:: html+django

        {# the current selected page #}
        {{ pages.current }}

        {# the first page #}
        {{ pages.first }}

        {# the last page #}
        {{ pages.last }}

        {# the previous page (or nothing if you are on first page) #}
        {{ pages.previous }}

        {# the next page (or nothing if you are in last page) #}
        {{ pages.next }}

        {# the third page #}
        {{ pages.3 }}
        {# this means page.1 is the same as page.first #}

        {# the 1-based index of the first item on the current page #}
        {{ pages.current_start_index }}

        {# the 1-based index of the last item on the current page #}
        {{ pages.current_end_index }}

        {# the total number of objects, across all pages #}
        {{ pages.total_count }}

        {# the first page represented as an arrow #}
        {{ pages.first_as_arrow }}

        {# the last page represented as an arrow #}
        {{ pages.last_as_arrow }}

    - iterate over *pages* to get all pages:

    .. code-block:: html+django

        {% for page in pages %}
            {# display page link #}
            {{ page }}

            {# the page url (beginning with "?") #}
            {{ page.url }}

            {# the page path #}
            {{ page.path }}

            {# the page number #}
            {{ page.number }}

            {# a string representing the page (commonly the page number) #}
            {{ page.label }}

            {# check if the page is the current one #}
            {{ page.is_current }}

            {# check if the page is the first one #}
            {{ page.is_first }}

            {# check if the page is the last one #}
            {{ page.is_last }}
        {% endfor %}

    You can change the variable name, e.g.:

    .. code-block:: html+django

        {% get_pages as page_links %}

    Must be called after ``{% paginate objects %}``.
    """
    # Validate args.
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        var_name = 'pages'
    else:
        args = args.split()
        if len(args) == 2 and args[0] == 'as':
            var_name = args[1]
        else:
            msg = 'Invalid arguments for %r tag' % tag_name
            raise template.TemplateSyntaxError(msg)
    # Call the node.
    return GetPagesNode(var_name)


class GetPagesNode(template.Node):
    """Add the page list to context."""

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        # This template tag could raise a PaginationError: you have to call
        # *paginate* or *lazy_paginate* before including the getpages template.
        data = utils.get_data_from_context(context)
        # Add the PageList instance to the context.
        context[self.var_name] = models.PageList(
            context['request'],
            data['page'],
            data['querystring_key'],
            default_number=data['default_number'],
            override_path=data['override_path'],
            context=context
        )
        return ''


@register.tag
def show_pages(parser, token):
    """Show page links.

    Usage:

    .. code-block:: html+django

        {% show_pages %}

    It is just a shortcut for:

    .. code-block:: html+django

        {% get_pages %}
        {{ pages }}

    You can set ``ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` in your *settings.py*
    to a callable, or to a dotted path representing a callable, used to
    customize the pages that are displayed.

    See the *__unicode__* method of ``endless_pagination.models.PageList`` for
    a detailed explanation of how the callable can be used.

    Must be called after ``{% paginate objects %}``.
    """
    # Validate args.
    if len(token.contents.split()) != 1:
        msg = '%r tag takes no arguments' % token.contents.split()[0]
        raise template.TemplateSyntaxError(msg)
    # Call the node.
    return ShowPagesNode()


class ShowPagesNode(template.Node):
    """Show the pagination."""

    def render(self, context):
        # This template tag could raise a PaginationError: you have to call
        # *paginate* or *lazy_paginate* before including the getpages template.
        data = utils.get_data_from_context(context)
        # Return the string representation of the sequence of pages.
        pages = models.PageList(
            context['request'],
            data['page'],
            data['querystring_key'],
            default_number=data['default_number'],
            override_path=data['override_path'],
            context=context
        )
        return utils.text(pages)


@register.tag
def show_current_number(parser, token):
    """Show the current page number, or insert it in the context.

    This tag can for example be useful to change the page title according to
    the current page number.

    To just show current page number:

    .. code-block:: html+django

        {% show_current_number %}

    If you use multiple paginations in the same page, you can get the page
    number for a specific pagination using the querystring key, e.g.:

    .. code-block:: html+django

        {% show_current_number using mykey %}

    The default page when no querystring is specified is 1. If you changed it
    in the `paginate`_ template tag, you have to call  ``show_current_number``
    according to your choice, e.g.:

    .. code-block:: html+django

        {% show_current_number starting from page 3 %}

    This can be also achieved using a template variable you passed to the
    context, e.g.:

    .. code-block:: html+django

        {% show_current_number starting from page page_number %}

    You can of course mix it all (the order of arguments is important):

    .. code-block:: html+django

        {% show_current_number starting from page 3 using mykey %}

    If you want to insert the current page number in the context, without
    actually displaying it in the template, use the *as* argument, i.e.:

    .. code-block:: html+django

        {% show_current_number as page_number %}
        {% show_current_number
            starting from page 3 using mykey as page_number %}

    """
    # Validate args.
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        key = None
        number = None
        tag_name = token.contents[0]
        var_name = None
    else:
        # Use a regexp to catch args.
        match = SHOW_CURRENT_NUMBER_EXPRESSION.match(args)
        if match is None:
            msg = 'Invalid arguments for %r tag' % tag_name
            raise template.TemplateSyntaxError(msg)
        # Retrieve objects.
        groupdict = match.groupdict()
        key = groupdict['key']
        number = groupdict['number']
        var_name = groupdict['var_name']
    # Call the node.
    return ShowCurrentNumberNode(number, key, var_name)


class ShowCurrentNumberNode(template.Node):
    """Show the page number taken from context."""

    def __init__(self, number, key, var_name):
        # Retrieve the page number.
        self.page_number_variable = None
        if number is None:
            self.page_number = 1
        elif number.isdigit():
            self.page_number = int(number)
        else:
            self.page_number_variable = template.Variable(number)

        # Get the queystring key.
        self.querystring_key_variable = None
        if key is None:
            self.querystring_key = settings.PAGE_LABEL
        elif key[0] in ('"', "'") and key[-1] == key[0]:
            self.querystring_key = key[1:-1]
        else:
            self.querystring_key_variable = template.Variable(key)

        # Get the template variable name.
        self.var_name = var_name

    def render(self, context):
        # Get the page number to use if it is not specified in querystring.
        if self.page_number_variable is None:
            default_number = self.page_number
        else:
            default_number = int(self.page_number_variable.resolve(context))

        # User can override the querystring key to use in the template.
        # The default value is defined in the settings file.
        if self.querystring_key_variable is None:
            querystring_key = self.querystring_key
        else:
            querystring_key = self.querystring_key_variable.resolve(context)

        # The request object is used to retrieve the current page number.
        page_number = utils.get_page_number_from_request(
            context['request'], querystring_key, default=default_number)

        if self.var_name is None:
            return utils.text(page_number)
        context[self.var_name] = page_number
        return ''
