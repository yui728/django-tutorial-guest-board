from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.remote import webelement
from selenium.webdriver.common.keys import Keys
import time
import chromedriver_binary
from selenium.webdriver.chrome.options import Options

class LiveChromeTest(StaticLiveServerTestCase):
    fixtures = ['posting_data']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('--headless')
        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def __assert_posting_panel(self, web_element: webelement.WebElement, posting_data: dict) -> None:
        title = web_element.find_element_by_css_selector('div.panel-heading > h3.panel-title')
        self.assertTrue(posting_data['name'] in title.text)
        created_at = web_element.find_element_by_css_selector('div.panel-heading > h3.panel-title > label.small')
        self.assertTrue(posting_data['created_at'] in created_at.text)
        message = web_element.find_element_by_css_selector('div.panel-body')
        self.assertEqual(posting_data['message'], message.text.strip())


    def test_guestboard_view_01(self):
        """Test Guest-Board First Access"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))
        self.assertEqual('Guest Board', self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_css_selector('input[name="name"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('textarea[name="message"]'))
        with self.assertRaises(selenium_exceptions.NoSuchElementException):
            self.assertFalse(self.selenium.find_element_by_css_selector('input[name="created_at"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('input.btn-primary[type="submit"][value="登録"]'))
        # Nextページリンクのチェック
        next_links = self.selenium.find_elements_by_css_selector('li.next')
        self.assertEquals(2, len(next_links))
        for next_link in next_links:
            self.assertTrue(next_link.get_attribute('class') not in 'disabled')
        # Previousページリンクのチェック
        previous_links = self.selenium.find_elements_by_css_selector('li.previous')
        self.assertEquals(2, len(previous_links))
        for previous_link in previous_links:
            self.assertTrue(previous_link.get_attribute('class') in 'disabled')
        # 投稿パネルの表示内容チェック
        postings = self.selenium.find_elements_by_css_selector('div.panel')
        self.assertEqual(5, len(postings))
        
        posting_data = {
            "name": "Tina",
            "created_at": "2019年2月1日19:45",
            "message": "Message 05"
        }
        self.__assert_posting_panel(postings[0], posting_data)

        posting_data = {
                "name": "Sam",
                "created_at": "2019年1月10日15:10",
                "message": "Message 04"
            }
        self.__assert_posting_panel(postings[1], posting_data)

        posting_data = {
            "name": "Hellen",
            "created_at": "2019年1月2日5:25",
            "message": "Message 03"
        }
        self.__assert_posting_panel(postings[2], posting_data)

        posting_data = {
            "name": "Mimi",
            "created_at": "2019年1月1日11:30",
            "message": "Message 02"
        }
        self.__assert_posting_panel(postings[3], posting_data)

        posting_data = {
            "name": "Paul",
            "created_at": "2019年1月1日10:10",
            "message": "Message 01"
        }
        self.__assert_posting_panel(postings[4], posting_data)

    def test_guestboard_view_02(self):
        """Click Top `Older` Button"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))
        next_links = self.selenium.find_elements_by_css_selector('li.next > a')
        self.assertEqual(2, len(next_links))
        next_url = next_links[0].get_attribute('href')
        next_links[0].click()
        time.sleep(10)
        self.assertEquals(next_url, self.selenium.current_url)

    def test_guestboard_view_03(self):
        """Click Bottom `Older` Button"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))
        next_links = self.selenium.find_elements_by_css_selector('li.next > a')
        self.assertEqual(2, len(next_links))
        next_url = next_links[1].get_attribute('href')
        next_links[1].click()
        time.sleep(10)
        self.assertEquals(next_url, self.selenium.current_url)

    def test_guestboard_view_04(self):
        """Click Top 'Newer' Button"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/?page=2'))
        next_links = self.selenium.find_elements_by_css_selector('li.previous > a')
        self.assertEqual(2, len(next_links))
        next_url = next_links[0].get_attribute('href')
        next_links[0].click()
        time.sleep(10)
        self.assertEquals(next_url, self.selenium.current_url)

    def test_guestboard_view_05(self):
        """Click Bottom 'Newer' Button"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/?page=2'))
        next_links = self.selenium.find_elements_by_css_selector('li.previous > a')
        self.assertEqual(2, len(next_links))
        next_url = next_links[1].get_attribute('href')
        next_links[1].click()
        time.sleep(10)
        self.assertEquals(next_url, self.selenium.current_url)