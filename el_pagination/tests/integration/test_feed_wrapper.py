"""Twitter-style pagination feeding an specific content wrapper integration tests."""



import el_pagination.settings
from el_pagination.tests.integration import SeleniumTestCase


class FeedWrapperPaginationTest(SeleniumTestCase):

    view_name = 'feed-wrapper'
    selector = 'tbody > tr > td:first-child'

    def test_new_elements_loaded(self):
        # Ensure a new page is loaded on click.
        self.get()
        with self.assertNewElements('object', range(1, 21)):
            self.click_link(self.MORE)

    def test_url_not_changed(self):
        # Ensure the request is done using Ajax (the page does not refresh).
        self.get()
        with self.assertSameURL():
            self.click_link(self.MORE)

    def test_direct_link(self):
        # Ensure direct links work.
        self.get(page=3)
        self.assertElements('object', range(21, 31))
        self.assertIn('page=3', self.selenium.current_url)

    def test_subsequent_page(self):
        # Ensure next page is correctly loaded in a subsequent page.
        self.get(page=2)
        with self.assertNewElements('object', range(11, 31)):
            self.click_link(self.MORE)

    def test_feed_wrapper__test_multiple_show_more_through_all_pages(self):
        # Make a 404 error when page is empty
        el_pagination.settings.PAGE_OUT_OF_RANGE_404 = True

        # Ensure new pages are loaded again and again.
        self.get()
        for page in range(2, 6):
            expected_range = range(1, 10 * page + 1)
            with self.assertSameURL():
                with self.assertNewElements('object', expected_range):
                    self.click_link(self.MORE)

                    # The more link is kept even in the last page, once it
                    # doesn't know it is the last
                    self.asserLinksEqual(1, self.MORE)

        # After one more click, the more link itself is removed
        self.click_link(self.MORE)
        self.asserLinksEqual(0, self.MORE)

        # Return to initial condition
        el_pagination.settings.PAGE_OUT_OF_RANGE_404 = False

    def test_no_more_link_in_last_page_opened_directly(self):
        self.get(page=5)
        self.asserLinksEqual(0, self.MORE)
        self.assertElements('object', range(41, 51))
