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
		  help_text='Enter email addresses one per line (XXX THIS DOES NOT DO ANYTHING YET BUT IT SHOULD ADD NEW USER ACCOUNTS If CORRESPONDING EMAIL DOES NOT EXIST IN SYSTEM)', \
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

  # require event date to be at least one day after today
  def validate_is_future_event(self, v):
    if v > datetime.datetime.now().date():
      return v
    raise ValidationError('Event must be after today')


  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    self.fields['date'].help_text = 'Use yyyy-mm-dd format'
    self.fields['time_start'].help_text = 'Use hh:mm:ss format'
    self.fields['date'].validators=[self.validate_is_future_event]
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



class RecipientWishListWithGiftForm(Form):
  wishlist_recipient = IntegerField(widget=widgets.HiddenInput)
  gift_id = IntegerField(widget=widgets.HiddenInput, required=False)
  wishlist_id = IntegerField(widget=widgets.HiddenInput, required=False)
  gift_name = CharField()
  gift_value = DecimalField(max_digits=8)
  wishlist_active = BooleanField(initial=True,required=False)


class AttendeeBudgetForm(Form):
  attendee = IntegerField(widget=widgets.HiddenInput, required=True)
  event = IntegerField(widget=widgets.HiddenInput, required=True)
  maxpurchases = DecimalField(max_digits=8, required=True, help_text="Specify zero to have an unlimited budget")
    

# could try using a modelformset for these instead...maybe next time
class AttendeeGiftsForm(Form):
  attendee = IntegerField(widget=widgets.HiddenInput, required=True)
  event = IntegerField(widget=widgets.HiddenInput, required=True)
  gifts = MultipleChoiceField(widget=widgets.CheckboxSelectMultiple, required=False)

  # set choices in calling view, rather than as init arg...
  """
  def __init__(self, queryset=None, *args, **kwargs):
    super(AttendeeGiftsForm, self).__init__(*args, **kwargs)
    if queryset is None:
      queryset = Gift.objects.all()
    choices = [ (x.id, x) for x in queryset ]
    self.fields['gifts'].choices = choices
    #self.fields['gifts'] = ModelMultipleChoiceField( \
    #			      widget=widgets.CheckboxSelectMultiple, \
    #			      queryset=queryset)
  """
  
  def clean_gifts(self):
    if len(self.cleaned_data['gifts']) > 2:
      raise ValidationError('No more than two gifts');
    return self.cleaned_data['gifts']

  

class AuthLoginForm(Form):
  username = EmailField(help_text="The e-mail address you " + \
				  "supplied on registration, or the " + \
				  "e-mail address you received an event " + \
				  "notification from.")
  password = CharField(widget=widgets.PasswordInput(render_value=False))



class AuthRegisterForm(Form):
  email = EmailField()
  password = CharField(widget=widgets.PasswordInput(render_value=False))
  user_type = ChoiceField(choices=UserProfile.GR_USER_TYPES_CHOICES)




