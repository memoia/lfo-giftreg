# IMM4LFO 2011-09-19
#

from gr.models import *
from django.forms import *
import datetime, time

class EventForm(ModelForm):
  class Meta:
    model = Event
  # TODO will need to block selection of recipient
  recipient = ModelChoiceField( \
		  queryset=User.objects.filter( \
		      userprofile__gr_user_type__exact='RCP'))
  attendees = ModelMultipleChoiceField( \
		  queryset=User.objects.filter( \
		      userprofile__gr_user_type__exact='ATT'), \
		  help_text='Control-click/command-click to select multiple', \
		  required = False)
  other_attendees = CharField(widget=Textarea, \
		  help_text='Enter email addresses one per line', \
		  required = False)

  """
  def validate_date(self, v):
    try:
      fmt = "%Y-%m-%d"
      r = datetime.datetime.fromtimestamp(time.mktime(time.strptime(v, fmt)))
    except Exception, details:
      raise ValidationError('Date not in proper format')
    return v

  def validate_time(self, v):
    try:
      fmt = "%H:%M:%S"
      r = datetime.datetime.fromtimestamp(time.mktime(time.strptime(v, fmt)))
    except:
      raise ValidationError('Time not in proper format')
    return v
  """

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    self.fields['date'].help_text = 'Use yyyy-mm-dd format'
    self.fields['time_start'].help_text = 'Use hh:mm:ss format'
    # apparently django does this automatically.
    #self.fields['date'].validators=[self.validate_date]
    #self.fields['time_start'].validators=[self.validate_time]
    #self.fields['time_end'].validators=[self.validate_time]
    
  """
  from django.contrib.admin.widgets import *
  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    self.fields['date'].widget = AdminDateWidget()
    self.fields['time_start'].widget = AdminTimeWidget()
    self.fields['time_end'].widget = AdminTimeWidget()
  """

