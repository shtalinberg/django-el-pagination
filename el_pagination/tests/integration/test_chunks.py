"""On scroll chunks integration tests."""

from __future__ import unicode_literals

from endless_pagination.tests.integration import SeleniumTestCase


class ChunksPaginationTest(SeleniumTestCase):

    view_name = 'chunks'

    def test_new_elements_loaded(self):
        # Ensure new pages are loaded on scroll.
        self.get()
        with self.assertNewElements('object', range(1, 11)):
            with self.assertNewElements('item', range(1, 11)):
                self.scroll_down()

    def test_url_not_changed(self):
        # Ensure the request is done using Ajax (the page does not refresh).
        self.get()
        with self.assertSameURL():
            self.scroll_down()

    def test_direct_link(self):
        # Ensure direct links work.
        self.get(data={'page': 2, 'items-page': 3})
        current_url = self.selenium.current_url
        self.assertElements('object', range(6, 11))
        self.assertElements('item', range(11, 16))
        self.assertIn('page=2', current_url)
        self.assertIn('items-page=3', current_url)

    def test_subsequent_page(self):
        # Ensure next page is correctly loaded in a subsequent page, even if
        # normally it is the last page of the chunk.
        self.get(page=3)
        with self.assertNewElements('object', range(11, 21)):
            self.scroll_down()

    def test_chunks(self):
        # Ensure new items are not loaded on scroll if the chunk is complete.
        self.get()
        for i in range(5):
            self.scroll_down()
            self.wait_ajax()
        self.assertElements('object', range(1, 16))
        self.assertElements('item', range(1, 21))
