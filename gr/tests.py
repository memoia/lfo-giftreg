# IMM4LFO 2011-09-18
#

from django.test import TestCase
from gr.models import *
from django.contrib.auth.models import User



class UserManagement(TestCase):
  def setUp(self):
    pass

  def testAddRecipient(self):
    u = {
	'username':	'rcp'
      ,	'first_name':	'Recipient'
      , 'last_name':	'One'
      , 'is_active':	True
    }
    r = User.objects.create(**u)
    p = r.get_profile()
    p.gr_user_type = 'RCP'
    p.save()
    s = User.objects.filter(username__exact='rcp', \
			    userprofile__gr_user_type__exact='RCP')
    self.failUnlessEqual(len(s), 1)

  def testAddAttendee(self):
    u = {
	'username':	'att'
      ,	'first_name':	'Attendee'
      , 'last_name':	'One'
      , 'is_active':	True
    }
    a = User.objects.create(**u)
    p = a.get_profile()
    p.gr_user_type = 'ATT'
    p.save()
    s = User.objects.filter(username__exact='att', \
			    userprofile__gr_user_type__exact='ATT')
    self.failUnlessEqual(len(s), 1)




"""
class RecipientWishList(TestCase):
  def setUp(self):
    self.gift1 = Gift.objects.create(name='Gift One', value=1.00)
    self.gift2 = Gift.objects.create(name='Gift Two', value=2.00)

  def testAddGift(self):
    pass

  def testRemoveGift(self):
    self.failUnlessEqual(1 + 1, 2)
"""

