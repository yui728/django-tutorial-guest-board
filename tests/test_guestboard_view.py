from with_asserts.case import TestCase
import guestboard.views as views
import string
from django.core.paginator import Page

class GuestboardViewTest(TestCase):
    fixtures = ['posting_data']

    def __assert_posting_panel(self, panel, posting_data):
        panel_head = panel.find('div.panel-heading')
        print("panel_head = {}".format(panel_head))
        self.assertEquals(posting_data["name"], panel_head.find('h3.panel-title').text)
        self.assertEquals(posting_data["created_at"], panel_head.find('h3-panel-title label.small').text)
        panel_body = panel.find('div.panel-body')
        self.assertEquals(posting_data["message"], panel_body.text)
 
    def test_view_index_access_01(self):
        """Show Get Page view"""
        response = self.client.get('/guestboard/', {})
        # print("response : {}".format(response.context))
        self.assertTemplateUsed(response, 'guestboard/index.html')
        with self.assertHTML(response, 'div.panel') as panels:
            self.assertEquals(5, len(panels))
            posting_data = {
                "name": "Alice",
                "created_at": "2019年1月1日 10:00",
                "message": "Hello!"
            }
            print(panels[0])
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


