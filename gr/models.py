# IMM4LFO 2011-09-16
#

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


def val_posint(s):
  """ alt use django.core.validators.MinValueValidator see pg 906 """
  try:
    if float(s) < 0:
      raise Exception
  except:
    raise ValidationError(u'Positive value required (you gave: "%s")' % s)



class UserProfile(models.Model):
  """ django.pdf pg 237 """
  user = models.OneToOneField(User)

  GR_USER_TYPES_CHOICES = (
      ('RCP','Recipient')
    , ('ATT','Attendee')
    , ('OTH','Other')
  )
  gr_user_type = models.CharField(default='OTH', \
				  max_length=3, \
				  choices=GR_USER_TYPES_CHOICES)

def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)



class Event(models.Model):
  recipient   = models.OneToOneField(User)
  attendees   = models.ManyToManyField(User, related_name='+')
  date	      = models.DateField(null=False, blank=False, db_index=True)
  time_start  = models.TimeField(null=False, blank=True)
  time_end    = models.TimeField(null=False, blank=True)
  name	      = models.CharField(max_length=255, \
				  null=False, \
				  blank=False, \
				  db_index=True, \
				  unique=True)
  location    = models.TextField(null=False, blank=False)
  details     = models.TextField(null=False, blank=True)


class Gift(models.Model):
  name = models.CharField(max_length=255, \
			  null=False, \
			  blank=False, \
			  db_index=True, \
			  unique=True)
  value = models.DecimalField(decimal_places=2, \
			      max_digits=8, \
			      validators=[val_posint])

class RecipientWishList(models.Model):
  recipient = models.ForeignKey(User)
  gift = models.ForeignKey(Gift)
  active = models.BooleanField(blank=False, default=True)

class AttendeeBudget(models.Model):
  attendee = models.ForeignKey(User)
  event = models.ForeignKey(Event)
  maxpurchases = models.DecimalField(decimal_places=2, \
			      max_digits=8, \
			      validators=[val_posint])

  def save(self, *args, **kwargs):
    # uniq constraint on (attendee,event) """
    c = AttendeeBudget.objects.filter(attendee__exact=attendee, \
				      event__exact=event)
    if len(c)>0:
      raise Exception("Budget attendee=%s, event=%s exists" % (attendee,event))
    super(AttendeeBudget, self).save(*args, **kwargs)


class AttendeeGifts(models.Model):
  attendee = models.ForeignKey(User)
  event = models.ForeignKey(Event)
  gift = models.ForeignKey(Gift)
  


# I wanted to split all the models into separate files.
# To do this, create models directory, create separate
# model files in there, and then in the __init__.py
# for the models dir, place from...import statements.
# also modify models to include class Meta: app_label
# ... the from...import statements for each file are annoying
# to have to maintain. tried automating this, didn't work out.
# Apparently splitting them up is bad practice since you should
# split things up by "app" instead.
"""
from userprofile import UserProfile
from event import Event
from gift import Gift
from recipientwishlist import RecipientWishList
from attendeebudget import AttendeeBudget
from attendeegifts import AttendeeGifts
"""
"""
import os, re

# there must be a better way to separate all models
#   into separate files and have them load normally,
#   without having to put from x import y statements
#   for each one in here manually....

# inspect and pyclbr not good here (first req import, second broken)
#
#__import__('UserProfile', fromlist=['userprofile'])
#   is supposed to emulate:
#from userprofile import UserProfile
#   but the former fails while the latter succeeds. 
#eval('from...') also doesn't work.

def model_files():
  return [os.path.dirname(__file__) + '/' + m for m in \
		filter(lambda x: x[:2]!='__' and x[-3:]=='.py' \
		  , os.listdir(os.path.dirname(__file__)))]

def classes(file_path):
  m = re.compile('^class (\w+).*')
  l = []
  with open(file_path, 'r') as f:
    for line in f:
      c = m.match(line)
      if c:
	l.append(c.groups(1)[0])
  return l

for mf in model_files():
  cl = classes(mf)
  for c in cl:
    print "from %s import %s" % (os.path.basename(mf[:-3]), c)
    #__import__(c, fromlist=[os.path.basename(mf[:-3])])
"""



