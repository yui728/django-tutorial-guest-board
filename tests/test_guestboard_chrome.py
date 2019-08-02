from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time

class LiveChromeTest(StaticLiveServerTestCase):
    fixtures = ['posting_data']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_first_view(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))