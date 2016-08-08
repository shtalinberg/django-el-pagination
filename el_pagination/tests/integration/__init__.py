"""Integration tests base objects definitions."""

from __future__ import unicode_literals
from contextlib import contextmanager
import os
import time
import unittest

from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver import Firefox
from selenium.webdriver.support import ui
from xvfbwrapper import Xvfb

from el_pagination.utils import PYTHON3


SHOW_BROWSER = os.getenv('SHOW_BROWSER', False)
SKIP_SELENIUM = os.getenv('SKIP_SELENIUM', False)
# FIXME: do not exclude integration tests on Python3 once Selenium is updated
# (bug #17).
tests_are_run = not (PYTHON3 or SKIP_SELENIUM)


def setup_package():
    """Set up the Selenium driver once for all tests."""
    # Just skipping *setup_package* and *teardown_package* generates an
    # uncaught exception under Python 2.6.
    if tests_are_run:
        if not SHOW_BROWSER:
            # Perform all graphical operations in memory.
            vdisplay = SeleniumTestCase.vdisplay = Xvfb(width=1280, height=720)
            vdisplay.start()
        # Create a Selenium browser instance.
        selenium = SeleniumTestCase.selenium = Firefox()
        selenium.maximize_window()
        SeleniumTestCase.wait = ui.WebDriverWait(selenium, 10)
        SeleniumTestCase.selenium.implicitly_wait(3)


def teardown_package():
    """Quit the Selenium driver."""
    if tests_are_run:
        SeleniumTestCase.selenium.quit()
        if not SHOW_BROWSER:
            SeleniumTestCase.vdisplay.stop()


# FIXME: do not exclude integration tests on Python3 once Selenium is updated
# (bug #17).
@unittest.skipIf(
    PYTHON3,
    'excluding integration tests: Python 3 tests are still not supported.')
@unittest.skipIf(
    SKIP_SELENIUM,
    'excluding integration tests: environment variable SKIP_SELENIUM is set.')
class SeleniumTestCase(StaticLiveServerTestCase):
    """Base test class for integration tests."""

    PREVIOUS = '<'
    NEXT = '>'
    MORE = 'More results'

    def setUp(self):
        self.url = self.live_server_url + reverse(self.view_name)

        # Give the browser a little time; Firefox sometimes throws
        # random errors if you hit it too soon
        # time.sleep(1)

#     @classmethod
#     def setUpClass(cls):
#         if not SHOW_BROWSER:
#             # start display
#             cls.xvfb = Xvfb(width=1280, height=720)
#             cls.xvfb.start()

#         # Create a Selenium browser instance.
#         cls.browser = os.getenv('SELENIUM_BROWSER', 'firefox')
#         # start browser
#         if cls.browser == 'firefox':
#             cls.selenium = webdriver.Firefox()
#         elif cls.browser == 'htmlunit':
#             cls.selenium = webdriver.Remote(desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)
#         elif cls.browser == 'iphone':
#             command_executor = "http://127.0.0.1:3001/wd/hub"
#             cls.selenium = webdriver.Remote(command_executor=command_executor,
#                 desired_capabilities=DesiredCapabilities.IPHONE)
#         elif cls.browser == 'safari':
#             cls.selenium = webdriver.Remote(desired_capabilities={
#                 "browserName": "safari", "version": "",
#                 "platform": "MAC", "javascriptEnabled": True})
#         else:
#             cls.selenium = webdriver.Chrome()
#         cls.selenium.maximize_window()
#         cls.wait = ui.WebDriverWait(cls.selenium, 10)
#         cls.selenium.implicitly_wait(3)
#
#         super(SeleniumTestCase, cls).setUpClass()

#     @classmethod
#     def tearDownClass(cls):
#         # stop browser
#         cls.selenium.quit()
#         super(SeleniumTestCase, cls).tearDownClass()
#         if not SHOW_BROWSER:
#             # stop display
#             cls.xvfb.stop()

    def get(self, url=None, data=None, **kwargs):
        """Load a web page in the current browser session.

        If *url* is None, *self.url* is used.
        The querydict can be expressed providing *data* or *kwargs*.
        """
        if url is None:
            url = self.url

        querydict = QueryDict('', mutable=True)
        if data is not None:
            querydict.update(data)
        querydict.update(kwargs)
        path = '{0}?{1}'.format(url, querydict.urlencode())

        # the following javascript scrolls down the entire page body.  Since Twitter
        # uses "inifinite scrolling", more content will be added to the bottom of the
        # DOM as you scroll... since it is in the loop, it will scroll down up to 100
        # times.
        # for _ in range(100):
        #     self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # print all of the page source that was loaded
        # print self.selenium.page_source.encode("utf-8")
        return self.selenium.get(path)

    def wait_ajax(self):
        """Wait for the document to be ready."""
        time.sleep(10)
        def document_ready(driver):
            script = """
                return (
                    document.readyState === 'complete' &&
                    jQuery.active === 0 &&
                    typeof jQuery != 'undefined'
                );
            """
            return driver.execute_script(script)
        self.wait.until(document_ready)
        return self.wait

    def click_link(self, text, index=0):
        """Click the link with the given *text* and *index*."""
        link = self.selenium.find_elements_by_link_text(str(text))[index]
        link.click()
        return link

    def scroll_down(self):
        """Scroll down to the bottom of the page."""
        script = 'window.scrollTo(0, document.body.scrollHeight);'
        self.selenium.execute_script(script)

    def get_current_elements(self, class_name, driver=None):
        """Return the range of current elements as a list of numbers."""
        elements = []
        selector = 'div.{0} > h4'.format(class_name)
        if driver is None:
            driver = self.selenium
        for element in driver.find_elements_by_css_selector(selector):
            elements.append(int(element.text.split()[1]))
        return elements

    def asserLinksEqual(self, count, text):
        """Assert the page contains *count* links with given *text*."""
        links = self.selenium.find_elements_by_link_text(str(text))
        self.assertEqual(count, len(links))

    def assertElements(self, class_name, elements):
        """Assert the current page contains the given *elements*."""
        current_elements = self.get_current_elements(class_name)
        self.assertSequenceEqual(
            elements, current_elements, (
                'Elements differ: {expected} != {actual}\n'
                'Class name: {class_name}\n'
                'Expected elements: {expected}\n'
                'Actual elements: {actual}'
            ).format(
                actual=current_elements,
                expected=elements,
                class_name=class_name,
            )
        )

    @contextmanager
    def assertNewElements(self, class_name, new_elements):
        """Fail when new elements are not found in the page."""
        def new_elements_loaded(driver):
            elements = self.get_current_elements(class_name, driver=driver)
            return elements == new_elements
        yield
        try:
            self.wait_ajax().until(new_elements_loaded)
        except exceptions.TimeoutException:
            self.assertElements(class_name, new_elements)

    @contextmanager
    def assertSameURL(self):
        """Assert the URL does not change after executing the yield block."""
        current_url = self.selenium.current_url
        yield
        self.wait_ajax()
        self.assertEqual(current_url, self.selenium.current_url)
