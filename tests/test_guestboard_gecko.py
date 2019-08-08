from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.remote import webelement
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options
from guestboard.models import Posting
from django.utils import dateformat
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LiveChromeTest(StaticLiveServerTestCase):
    fixtures = ['posting_data']
    SERVER_RESPONSE_WAIT_SEC = 10

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('-headless')
        cls.selenium = webdriver.Firefox(firefox_options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def __assert_posting_panel(self, web_element: webelement.WebElement, posting_data: dict) -> None:
        title = web_element.find_element_by_css_selector('div.panel-heading > h3.panel-title')
        if 'name' in posting_data.keys():
            self.assertTrue(posting_data['name'] in title.text)
        created_at = web_element.find_element_by_css_selector('div.panel-heading > h3.panel-title > label.small')
        if 'created_at' in posting_data.keys():
            self.assertTrue(posting_data['created_at'] in created_at.text)
        message = web_element.find_element_by_css_selector('div.panel-body')
        if 'messsage' in posting_data.keys():
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
            self.assertTrue('disabled' not in next_link.get_attribute('class'))
        # Previousページリンクのチェック
        previous_links = self.selenium.find_elements_by_css_selector('li.previous')
        self.assertEquals(2, len(previous_links))
        for previous_link in previous_links:
            self.assertTrue('disabled' in previous_link.get_attribute('class'))
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

    def test_guestboard_click_next_01(self):
        """Click Top `Older` Button"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))
        next_links = self.selenium.find_elements_by_css_selector('li.next > a')
        self.assertEqual(2, len(next_links))
        next_url = next_links[0].get_attribute('href')
        next_links[0].click()
        time.sleep(self.SERVER_RESPONSE_WAIT_SEC)
        self.assertEquals(next_url, self.selenium.current_url)

    def test_guestboard_click_next_02(self):
        """Click Bottom `Older` Button"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))
        next_links = self.selenium.find_elements_by_css_selector('li.next > a')
        self.assertEqual(2, len(next_links))
        next_url = next_links[1].get_attribute('href')
        next_links[1].click()
        time.sleep(self.SERVER_RESPONSE_WAIT_SEC)
        self.assertEquals(next_url, self.selenium.current_url)

    def test_guestboard_click_previous_01(self):
        """Click Top 'Newer' Button"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/?page=2'))
        previous_links = self.selenium.find_elements_by_css_selector('li.previous > a')
        self.assertEqual(2, len(previous_links))
        previous_url = previous_links[0].get_attribute('href')
        previous_links[0].click()
        time.sleep(self.SERVER_RESPONSE_WAIT_SEC)
        self.assertEquals(previous_url, self.selenium.current_url)

    def test_guestboard_click_previous_02(self):
        """Click Bottom 'Newer' Button"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/?page=2'))
        previous_links = self.selenium.find_elements_by_css_selector('li.previous > a')
        self.assertEqual(2, len(previous_links))
        previous_url = previous_links[1].get_attribute('href')
        previous_links[1].click()
        time.sleep(self.SERVER_RESPONSE_WAIT_SEC)
        self.assertEquals(previous_url, self.selenium.current_url)

    def test_guestboard_check_disabled_next_button_01(self):
        """Check Oldest Page in Diasbled `next` link"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/?page=2'))
        next_links = self.selenium.find_elements_by_css_selector('li.next')
        self.assertEqual(2, len(next_links))
        for next_link in next_links:
            self.assertTrue('disabled' in next_link.get_attribute('class'))

    def test_guestboard_submit_01(self):
        """Posting input error for name and message no input"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))
        submit = self.selenium.find_element_by_css_selector('input[type="submit"]')
        submit.click()
        time.sleep(self.SERVER_RESPONSE_WAIT_SEC)
        # 名前とメッセージを未入力でSubmitしようとすると、名前にフォーカスする
        actived = self.selenium.switch_to_active_element()
        self.assertEqual('input', actived.tag_name)
        self.assertEqual('text', actived.get_attribute('type'))
        self.assertEqual('name', actived.get_attribute('name'))

    def test_guestboard_submit_02(self):
        """Posting input error for name no input"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))
        # input message
        message = self.selenium.find_element_by_css_selector('textarea[name="message"]')
        submit = self.selenium.find_element_by_css_selector('input[type="submit"]')
        message.send_keys("Test Message 100")
        message.send_keys(Keys.ENTER)
        submit.click()
        time.sleep(self.SERVER_RESPONSE_WAIT_SEC)
        # 名前を未入力でSubmitしようとすると、名前にフォーカスする
        actived = self.selenium.switch_to_active_element()
        self.assertEqual('input', actived.tag_name)
        self.assertEqual('text', actived.get_attribute('type'))
        self.assertEqual('name', actived.get_attribute('name'))

    def test_guestboard_submit_03(self):
        """Posting input error for message no input"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))
        # input name
        name = self.selenium.find_element_by_css_selector('input[name="name"]')
        submit = self.selenium.find_element_by_css_selector('input[type="submit"]')
        name.send_keys("Arty")
        name.send_keys(Keys.ENTER)
        submit.click()
        time.sleep(self.SERVER_RESPONSE_WAIT_SEC)
        # メッセージを未入力でSubmitしようとすると、メッセージにフォーカスする
        actived = self.selenium.switch_to_active_element()
        self.assertEqual('textarea', actived.tag_name)
        self.assertEqual('message', actived.get_attribute('name'))

    def test_guetstboard_submit_04(self):
        """Posting submit success and view registerd message"""
        self.selenium.get('%s%s' % (self.live_server_url, '/guestboard/'))
        # input name
        name = self.selenium.find_element_by_css_selector('input[name="name"]')
        name.send_keys("Arty")
        # input message
        message = self.selenium.find_element_by_css_selector('textarea[name="message"]')
        message.send_keys("Test Message 100")
        # click submit button
        submit = self.selenium.find_element_by_css_selector('input[type="submit"]')
        submit.click()
        # time.sleep(self.SERVER_RESPONSE_WAIT_SEC)
        # リダイレクトチェック
        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_to_be('%s%s' % (self.live_server_url, '/guestboard/')))
        # 投稿成功メッセージチェック
        messages = self.selenium.find_elements_by_css_selector('ul.messages > li.success')
        self.assertEqual(1, len(messages))
        self.assertEqual('投稿を受け付けました。', messages[0].text.strip())
        # 投稿パネルの表示内容チェック
        postings = self.selenium.find_elements_by_css_selector('div.panel')
        self.assertEqual(5, len(postings))
        posting_data = {
            "name": "Arty",
            "message": "Test Message 100",
        }
        self.__assert_posting_panel(postings[0], posting_data)


