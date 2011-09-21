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
  
  def is_recipient(self):
    return self.gr_user_type == 'RCP'

  def is_attendee(self):
    return self.gr_user_type == 'ATT'

def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Event(models.Model):
  recipient   = models.OneToOneField(User)
  attendees   = models.ManyToManyField(User, related_name='+')
  date	      = models.DateField(null=False, blank=False, db_index=True)
  time_start  = models.TimeField(null=True, blank=True)
  time_end    = models.TimeField(null=True, blank=True)
  name	      = models.CharField(max_length=255, \
				  null=False, \
				  blank=False, \
				  db_index=True, \
				  unique=True)
  location    = models.TextField(null=False, blank=False)
  details     = models.TextField(null=False, blank=True)

  def save(self, *args, **kwargs):
    if not self.recipient.get_profile().is_recipient():
      raise Exception('Event host must be a recipient user')
    return super(Event, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.name


class Gift(models.Model):
  name = models.CharField(max_length=255, \
			  null=False, \
			  blank=False, \
			  db_index=True)
			  #unique=True)
  value = models.DecimalField(decimal_places=2, \
			      max_digits=8, \
			      validators=[val_posint])
  def __unicode__(self):
    return u"%s ($%s)" % (self.name, self.value)


class RecipientWishListManager(models.Manager):
  def attendee_options(self,recipient_id,attendee_id,event_id):
    """ available items for an attendee to pick from """
    available = super(RecipientWishListManager, self).get_query_set() \
		  .filter(recipient__id=recipient_id) \
		  .select_related(depth=1) \
		  .exclude(gift__attendeegifts__in= \
		    AttendeeGifts.objects.filter( \
		      models.Q(event__id=event_id), \
		      ~models.Q(attendee__id=attendee_id) \
		    ) \
		  ) \
		  .exclude( \
		    models.Q(active=False), \
		    ~models.Q(gift__attendeegifts__in= \
		      AttendeeGifts.objects.filter( \
			event__id=event_id, \
			attendee__id=attendee_id \
		      ) \
		    ) \
		  )
    return available

class RecipientWishList(models.Model):
  objects = RecipientWishListManager()
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
    # uniq constraint on (attendee,event)
    try:
      c = AttendeeBudget.objects.get(attendee__exact=self.attendee, \
				      event__exact=self.event)
      if c.id != self.id:
	raise Exception('Budget for this attendee/event already exists')
    except AttendeeBudget.DoesNotExist:
      pass
    return super(AttendeeBudget, self).save(*args, **kwargs)


class AttendeeGifts(models.Model):
  attendee = models.ForeignKey(User)
  event = models.ForeignKey(Event)
  gift = models.ForeignKey(Gift)

  def save(self, *args, **kwargs):
    # TODO prevent going over-budget
    return super(AttendeeGifts, self).save(*args, **kwargs)


