from django.test import TestCase

class GuestboardViewTest(TestCase):
    def test_view_index_01(self):
        """Show Get Page view"""
        response = self.client.get('guestboard/')
        self.assertTemplateUsed(response, 'guestboard/index.html')