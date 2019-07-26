from django.test import SimpleTestCase
from guestboard.forms import PostingForm

class PostingFormTest(SimpleTestCase):
    def test_form_success_01(self):
        """Form Validation Success Pattern"""
        form = PostingForm(
            {
                'name': "アリス",
                'message': "はじめまして。"
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_error_01(self):
        """Form Validation Error Pattern 01: name is not null"""
        form = PostingForm(
            {
                'name': "",
                'message': "Hi!"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertTrue("name" in form.errors.as_data())

    def test_form_error_02(self):
        """Form Validation Error Pattern 02: message is not null"""
        form = PostingForm(
            {
                'name': "Paul",
                'message': ""
            }
        )
        self.assertFalse(form.is_valid())
        self.assertTrue("message" in form.errors.as_data())