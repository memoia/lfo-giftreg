# IMM4LFO 2011-09-18
#

from django.test import TestCase
from django.db import IntegrityError
from gr.models import *
from django.contrib.auth.models import User
import datetime




class UserTest(TestCase):
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


class EventTest(TestCase):
  def setUp(self):
    self.user_notype = User.objects.create_user('etnotype','etnotype@localhost')
    def _make_users(user_type, amt):
      for n in range(1, amt+1):
	setattr(self, "user_%s%s"%(user_type,n), \
		  User.objects.create_user("et%s%s"%(user_type,n), \
				"et%s%s@localhost"%(user_type,n)))
	u = getattr(self, "user_%s%s"%(user_type,n))
	p = u.get_profile()
	p.gr_user_type = user_type.upper()
	p.save()
    _make_users('rcp', 2)
    _make_users('att', 4)
    self.base_event_struct = {
	'recipient': None
      , 'date': datetime.datetime.now()
      , 'name': 'Test Event'
      , 'location': 'Somewhere'
    }

  def testCreateEventByNonRecipient(self):
    x = dict(self.base_event_struct)
    x['recipient'] = self.user_notype
    x['name'] = 'Test Event Non Recip'
    e = Event(**x)
    self.assertRaises(Exception, e.save)

  def testCreateEventRecipientHasMoreThanOne(self):
    x = dict(self.base_event_struct)
    x['recipient'] = self.user_rcp1
    x['name'] = 'Test Event Recipgreedy1'
    y = dict(x)
    y['name'] = 'Test Event Recipgreedy2'
    e = Event(**x)
    e.save()
    f = Event(**y)
    self.assertRaises(IntegrityError, f.save)


class AttendeeBudgetTest(TestCase):
  def setUp(self):

    def _make_users(user_type, amt):
      for n in range(1, amt+1):
	setattr(self, "user_%s%s"%(user_type,n), \
		  User.objects.create_user("abt%s%s"%(user_type,n), \
				"abt%s%s@localhost"%(user_type,n)))
	u = getattr(self, "user_%s%s"%(user_type,n))
	p = u.get_profile()
	p.gr_user_type = user_type.upper()
	p.save()

    def _make_events(rcp_list):
      self.events = []
      x = {
	  'recipient': None
	, 'date': datetime.datetime.now()
	, 'name': 'Test Event'
	, 'location': 'Somewhere'
      }
      for r in rcp_list:
	x['recipient'] = r
	x['name'] = "Test Event By %s" % repr(r)
	e = Event(**x)
	self.events.append(e)
	e.save()

    _make_users('rcp', 3)
    _make_users('att', 4)
    _make_events([self.user_rcp1, self.user_rcp2])

  def testUniqOnAttendeeEvent(self):
    ab1 = AttendeeBudget(attendee=self.user_att1, event=self.events[0], maxpurchases='10.0')
    ab1.save()
    ab2 = AttendeeBudget(attendee=self.user_att1, event=self.events[0], maxpurchases='12.0')
    self.assertRaises(Exception, ab2.save)





# TODO add cases for additional checks added to models/managers





