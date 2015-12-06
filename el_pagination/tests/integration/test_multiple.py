"""Multiple pagination integration tests."""

from __future__ import unicode_literals

from endless_pagination.tests.integration import SeleniumTestCase


class MultiplePaginationTest(SeleniumTestCase):

    view_name = 'multiple'

    def test_new_elements_loaded(self):
        # Ensure a new page is loaded on click for each paginated elements.
        self.get()
        with self.assertNewElements('object', range(4, 7)):
            with self.assertNewElements('item', range(7, 10)):
                with self.assertNewElements('entry', range(1, 5)):
                    self.click_link(2, 0)
                    self.click_link(3, 1)
                    self.click_link(self.MORE)

    def test_url_not_changed(self):
        # Ensure the requests are done using Ajax (the page does not refresh).
        self.get()
        with self.assertSameURL():
            self.click_link(2, 0)
            self.click_link(3, 1)
            self.click_link(self.MORE)

    def test_direct_link(self):
        # Ensure direct links work.
        self.get(data={'objects-page': 3, 'items-page': 4, 'entries-page': 5})
        self.assertElements('object', range(7, 10))
        self.assertElements('item', range(10, 13))
        self.assertElements('entry', range(11, 14))
        self.assertIn('objects-page=3', self.selenium.current_url)
        self.assertIn('items-page=4', self.selenium.current_url)
        self.assertIn('entries-page=5', self.selenium.current_url)

    def test_subsequent_pages(self):
        # Ensure elements are correctly loaded starting from a subsequent page.
        self.get(data={'objects-page': 2, 'items-page': 2, 'entries-page': 2})
        with self.assertNewElements('object', range(1, 4)):
            with self.assertNewElements('item', range(7, 10)):
                with self.assertNewElements('entry', range(2, 8)):
                    self.click_link(self.PREVIOUS, 0)
                    self.click_link(self.NEXT, 1)
                    self.click_link(self.MORE)

    def test_no_more_link_in_last_page(self):
        # Ensure there is no more or forward links on the last pages.
        self.get(data={'objects-page': 7, 'items-page': 7, 'entries-page': 8})
        self.asserLinksEqual(0, self.NEXT)
        self.asserLinksEqual(0, self.MORE)
