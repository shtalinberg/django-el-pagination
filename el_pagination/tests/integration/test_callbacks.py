"""Javascript callbacks integration tests."""

from __future__ import unicode_literals

from endless_pagination.tests.integration import SeleniumTestCase


class CallbacksTest(SeleniumTestCase):

    view_name = 'callbacks'

    def notifications_loaded(self, driver):
        return driver.find_elements_by_id('fragment')

    def assertNotificationsEqual(self, notifications):
        """Assert the given *notifications* equal the ones in the DOM."""
        self.wait_ajax().until(self.notifications_loaded)
        find = self.selenium.find_element_by_id
        for key, value in notifications.items():
            self.assertEqual(value, find(key).text)

    def test_on_click(self):
        # Ensure the onClick callback is correctly called.
        self.get()
        self.click_link(2)
        self.assertNotificationsEqual({
            'onclick': 'Object 1',
            'onclick-label': '2',
            'onclick-url': '/callbacks/?page=2',
            'onclick-key': 'page',
        })

    def test_on_completed(self):
        # Ensure the onCompleted callback is correctly called.
        self.get(page=10)
        self.click_link(1)
        self.assertNotificationsEqual({
            'oncompleted': 'Object 1',
            'oncompleted-label': '1',
            'oncompleted-url': '/callbacks/',
            'oncompleted-key': 'page',
            'fragment': 'Object 3',
        })
