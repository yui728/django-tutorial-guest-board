from django.test import TestCase
from src.guestboard import Posting
from django.db import utils

class PostingModelTest(TestCase):
 def test_01(self):
     """"Create Success Pattern"""
     name = "aaa"
     message = "message01"
     Posting.objects.create(name=name, message=message)

 def test_02(self):
     """Create Error Pattern1: name is not null"""
     name = None
     message = "message01"
     with self.assertRaises(utils.IntegrityError):
         Posting.objects.create(name=name, message=message)

 def test_03(self):
    """Create Error Pattern3: mesage is not null"""
    name = "AAA"
    message = None
    with self.assertRaises(utils.IntegrityError):
        Posting.objects.create(name=name, message=message)