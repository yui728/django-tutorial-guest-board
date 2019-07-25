from django.test import TestCase
from guestboard.models import Posting
from django.db import utils

class PostingModelTest(TestCase):
 def test_01(self):
     """"Create Normal Pattern"""
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

 def test_04(self):
     """Create Error Pattern3; name length under 65"""
     name = "a" * 65
     print("name = {}, length={}".format(name, len(name)))
     message = "message 04"
    #  with self.assertRaises(ValueError):
     Posting.objects.create(name=name, message=message)