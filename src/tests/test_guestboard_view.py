from with_asserts.case import TestCase
from src import guestboard as views
import string
from django.core.paginator import Page

class GuestboardViewTest(TestCase):
    fixtures = ['posting_data']

    def __assert_posting_panel(self, panel, posting_data):
        # print("panel-childrens={}".format(panel.getchildren()))
        panel_head = panel.cssselect('div.panel-heading')
        self.assertIsNotNone(panel_head)
        self.assertNotEqual(0, len(panel_head))
        # print("panel_head = {}".format(panel_head))
        # print("panel-head={}".format(panel_head[0]))
        panel_title = panel_head[0].cssselect('h3.panel-title')
        self.assertIsNotNone(panel_title)
        self.assertNotEquals(0, len(panel_title))
        self.assertEquals(posting_data["name"], panel_title[0].text.rstrip())
        created_at = panel_title[0].cssselect('label.small')
        self.assertIsNotNone(created_at)
        self.assertNotEquals(0, len(created_at))
        self.assertTrue(posting_data["created_at"] in created_at[0].text)
        panel_body = panel.cssselect('div.panel-body')
        self.assertEquals(posting_data["message"], panel_body[0].text.strip())
 
    def test_view_index_access_01(self):
        """Show Get Page view"""
        response = self.client.get('/guestboard/', {})
        # print("response : {}".format(response.context))
        self.assertTemplateUsed(response, 'guestboard/index.html')
        with self.assertHTML(response, 'div.panel') as panels:
            self.assertEquals(5, len(panels))
            posting_data = {
                "name": "Tina",
                "created_at": "2019年2月1日19:45",
                "message": "Message 05"
            }
            self.__assert_posting_panel(panels[0], posting_data)

            posting_data = {
                "name": "Sam",
                "created_at": "2019年1月10日15:10",
                "message": "Message 04"
            }
            self.__assert_posting_panel(panels[1], posting_data)

            posting_data = {
                "name": "Hellen",
                "created_at": "2019年1月2日5:25",
                "message": "Message 03"
            }
            self.__assert_posting_panel(panels[2], posting_data)

            posting_data = {
                "name": "Mimi",
                "created_at": "2019年1月1日11:30",
                "message": "Message 02"
            }
            self.__assert_posting_panel(panels[3], posting_data)

            posting_data = {
                "name": "Paul",
                "created_at": "2019年1月1日10:10",
                "message": "Message 01"
            }
            self.__assert_posting_panel(panels[4], posting_data)

    def test_view_index_access_02(self):
        """Show Get Page view as set page-no."""
        response = self.client.get('/guestboard/', {"page": 2})
        # print("response : {}".format(response.context))
        self.assertTemplateUsed(response, 'guestboard/index.html')
        with self.assertHTML(response, 'div.panel') as panels:
            self.assertEquals(1, len(panels))
            posting_data = {
                "name": "Alice",
                "created_at": "2019年1月1日10:00",
                "message": "Hello!"
            }
            self.__assert_posting_panel(panels[0], posting_data)

    def test_view_get_page_01(self):
        """Call No PageNo return First Page."""
        list = string.ascii_letters
        page = views._get_page(list, None)
        self.assertIsNotNone(page)
        self.assertIsInstance(page, Page)
        self.assertEqual(5, len(page.object_list))
        self.assertEqual(1, page.number)
        self.assertTrue(page.has_next())
        self.assertFalse(page.has_previous())
        self.assertTrue(page.has_other_pages())
        self.assertIn("a", page.object_list)
        self.assertIn("b", page.object_list)
        self.assertIn("c", page.object_list)
        self.assertIn("d", page.object_list)
        self.assertIn("e", page.object_list)

    def test_view_get_page_02(self):
        """Call a PageNo return this Page."""
        list = string.ascii_letters
        page = views._get_page(list, 2)
        self.assertIsNotNone(page)
        self.assertIsInstance(page, Page)
        self.assertEqual(5, len(page.object_list))
        self.assertEqual(2, page.number)
        self.assertTrue(page.has_next())
        self.assertTrue(page.has_previous())
        self.assertTrue(page.has_other_pages())
        self.assertIn("f", page.object_list)
        self.assertIn("g", page.object_list)
        self.assertIn("h", page.object_list)
        self.assertIn("i", page.object_list)
        self.assertIn("j", page.object_list)

    def test_view_get_page_03(self):
        """Call pageno is no-integer return first Page."""
        list = string.ascii_letters
        page = views._get_page(list, "a")
        self.assertIsNotNone(page)
        self.assertIsInstance(page, Page)
        self.assertEqual(5, len(page.object_list))
        self.assertEqual(1, page.number)
        self.assertTrue(page.has_next())
        self.assertFalse(page.has_previous())
        self.assertTrue(page.has_other_pages())
        self.assertIn("a", page.object_list)
        self.assertIn("b", page.object_list)
        self.assertIn("c", page.object_list)
        self.assertIn("d", page.object_list)
        self.assertIn("e", page.object_list)

    def test_view_get_page_04(self):
        """Call pageno is out-of-page return first Page."""
        list = string.ascii_letters
        page = views._get_page(list, 999)
        self.assertIsNotNone(page)
        self.assertIsInstance(page, Page)
        self.assertEqual(5, len(page.object_list))
        self.assertEqual(1, page.number)
        self.assertTrue(page.has_next())
        self.assertFalse(page.has_previous())
        self.assertTrue(page.has_other_pages())
        self.assertIn("a", page.object_list)
        self.assertIn("b", page.object_list)
        self.assertIn("c", page.object_list)
        self.assertIn("d", page.object_list)
        self.assertIn("e", page.object_list)


