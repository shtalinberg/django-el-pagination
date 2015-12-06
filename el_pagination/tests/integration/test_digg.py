"""Digg-style pagination integration tests."""

from __future__ import unicode_literals

from el_pagination.tests.integration import SeleniumTestCase


class DiggPaginationTest(SeleniumTestCase):

    view_name = 'digg'

    def test_new_elements_loaded(self):
        # Ensure a new page is loaded on click.
        self.get()
        with self.assertNewElements('object', range(6, 11)):
            self.click_link(2)

    def test_url_not_changed(self):
        # Ensure the request is done using Ajax (the page does not refresh).
        self.get()
        with self.assertSameURL():
            self.click_link(2)

    def test_direct_link(self):
        # Ensure direct links work.
        self.get(page=4)
        self.assertElements('object', range(16, 21))
        self.assertIn('page=4', self.selenium.current_url)

    def test_next(self):
        # Ensure next page is correctly loaded.
        self.get()
        with self.assertSameURL():
            with self.assertNewElements('object', range(6, 11)):
                self.click_link(self.NEXT)

    def test_previous(self):
        # Ensure previous page is correctly loaded.
        self.get(page=4)
        with self.assertSameURL():
            with self.assertNewElements('object', range(11, 16)):
                self.click_link(self.PREVIOUS)

    def test_no_previous_link_in_first_page(self):
        # Ensure there is no previous link on the first page.
        self.get()
        self.asserLinksEqual(0, self.PREVIOUS)

    def test_no_next_link_in_last_page(self):
        # Ensure there is no forward link on the last page.
        self.get(page=10)
        self.asserLinksEqual(0, self.NEXT)
