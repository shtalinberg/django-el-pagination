"""Test project URL patterns."""

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path as url
from django.views.generic import TemplateView

from el_pagination.decorators import page_template, page_templates
from project.views import generic

# Avoid lint errors for the following Django idiom: ruff: noqa.
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(
        r'^complete/$',
        page_templates(
            {
                'complete/objects_page.html': 'objects-page',
                'complete/items_page.html': 'items-page',
                'complete/entries_page.html': 'entries-page',
                'complete/articles_page.html': 'articles-page',
            }
        )(generic),
        {'template': 'complete/index.html', 'number': 21},
        name='complete',
    ),
    url(
        r'^digg/$',
        page_template('digg/page.html')(generic),
        {'template': 'digg/index.html'},
        name='digg',
    ),
    url(
        r'^digg/table$',
        page_template('digg/table/page.html')(generic),
        {'template': 'digg/table/index.html'},
        name='digg-table',
    ),
    url(
        r'^twitter/$',
        page_template('twitter/page.html')(generic),
        {'template': 'twitter/index.html'},
        name='twitter',
    ),
    url(
        r'^twitter/table$',
        page_template('twitter/table/page.html')(generic),
        {'template': 'twitter/table/index.html'},
        name='twitter-table',
    ),
    url(
        r'^onscroll/$',
        page_template('onscroll/page.html')(generic),
        {'template': 'onscroll/index.html'},
        name='onscroll',
    ),
    url(
        r'^onscroll/table$',
        page_template('onscroll/table/page.html')(generic),
        {'template': 'onscroll/table/index.html'},
        name='onscroll-table',
    ),
    url(
        r'^feed-wrapper/$',
        page_template('feed_wrapper/page.html')(generic),
        {'template': 'feed_wrapper/index.html'},
        name='feed-wrapper',
    ),
    url(
        r'^chunks/$',
        page_templates(
            {
                'chunks/objects_page.html': None,
                'chunks/items_page.html': 'items-page',
            }
        )(generic),
        {'template': 'chunks/index.html', 'number': 50},
        name='chunks',
    ),
    url(
        r'^multiple/$',
        page_templates(
            {
                'multiple/objects_page.html': 'objects-page',
                'multiple/items_page.html': 'items-page',
                'multiple/entries_page.html': 'entries-page',
            }
        )(generic),
        {'template': 'multiple/index.html', 'number': 21},
        name='multiple',
    ),
    url(
        r'^callbacks/$',
        page_template('callbacks/page.html')(generic),
        {'template': 'callbacks/index.html'},
        name='callbacks',
    ),
]

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]

urlpatterns += staticfiles_urlpatterns()
