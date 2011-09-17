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
  

