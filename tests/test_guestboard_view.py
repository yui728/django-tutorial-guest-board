from django.test import TestCase
import guestboard.views as views
import string
from django.core.paginator import Page

class GuestboardViewTest(TestCase):
    def test_view_index_access_01(self):
        """Show Get Page view"""
        response = self.client.get('guestboard/')
        self.assertTemplateUsed(response, 'guestboard/index.html')

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


