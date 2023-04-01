"""View decorators for Ajax powered pagination."""

from functools import wraps

from el_pagination.settings import PAGE_LABEL, TEMPLATE_VARNAME

QS_KEY = "querystring_key"


def page_template(template, key=PAGE_LABEL):
    """Return a view dynamically switching template if the request is Ajax.

    Decorate a view that takes a *template* and *extra_context* keyword
    arguments (like generic views).
    The template is switched to *page_template* if request is ajax and
    if *querystring_key* variable passed by the request equals to *key*.
    This allows multiple Ajax paginations in the same page.
    The name of the page template is given as *page_template* in the
    extra context.
    """

    def decorator(view):
        @wraps(view)
        def decorated(request, *args, **kwargs):
            # Trust the developer: he wrote ``context.update(extra_context)``
            # in his view.
            extra_context = kwargs.setdefault("extra_context", {})
            extra_context["page_template"] = template
            # Switch the template when the request is Ajax.
            querystring_key = request.GET.get(
                QS_KEY, request.POST.get(QS_KEY, PAGE_LABEL)
            )
            if (
                request.headers.get("x-requested-with") == "XMLHttpRequest"
                and querystring_key == key
            ):
                kwargs[TEMPLATE_VARNAME] = template
            return view(request, *args, **kwargs)

        return decorated

    return decorator


def _get_template(querystring_key, mapping):
    """Return the template corresponding to the given ``querystring_key``."""
    default = None
    try:
        template_and_keys = mapping.items()
    except AttributeError:
        template_and_keys = mapping
    for template, key in template_and_keys:
        if key is None:
            key = PAGE_LABEL
            default = template
        if key == querystring_key:
            return template
    return default


def page_templates(mapping):
    """Like the *page_template* decorator but manage multiple paginations.

    You can map multiple templates to *querystring_keys* using the *mapping*
    dict, e.g.::

        @page_templates({
            'page_contents1.html': None,
            'page_contents2.html': 'go_to_page',
        })
        def myview(request):
            ...

    When the value of the dict is None then the default *querystring_key*
    (defined in settings) is used. You can use this decorator instead of
    chaining multiple *page_template* calls.
    """

    def decorator(view):
        @wraps(view)
        def decorated(request, *args, **kwargs):
            # Trust the developer: he wrote ``context.update(extra_context)``
            # in his view.
            extra_context = kwargs.setdefault("extra_context", {})
            querystring_key = request.GET.get(
                QS_KEY, request.POST.get(QS_KEY, PAGE_LABEL)
            )
            template = _get_template(querystring_key, mapping)
            extra_context["page_template"] = template
            # Switch the template when the request is Ajax.
            if request.headers.get("x-requested-with") == "XMLHttpRequest" and template:
                kwargs[TEMPLATE_VARNAME] = template
            return view(request, *args, **kwargs)

        return decorated

    return decorator
