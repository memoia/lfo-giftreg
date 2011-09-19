# IMM4LFO 2011-09-16
#

from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from datetime import datetime
from gr.models import *
from gr.forms import *

"""
from django.core.mail import send_mail
send_mail(subject, message, sender, recipients)
"""


def index(request):
  return render_to_response('gr/main.html', {})


def event_list(request):
  #events = Event.objects.all()	  # use objects.select_related()?
  events=Event.objects.filter(date__gte=datetime.now()).select_related(depth=1)
  return render_to_response('gr/event_list.html', {'events':events})

def event_view(request):
  pass


def event_edit(request, event_id=None):
  if request.method == 'POST':
    if len(request.POST['event_id']) > 0:
      event_id = request.POST['event_id']
      event = Event.objects.get(pk=event_id)
      form = EventForm(request.POST, instance=event)
    else:
      form = EventForm(request.POST)
    if form.is_valid():
      """
      if len(form.cleaned_data['event_id']) > 0:
	event_id = form.cleaned_data['event_id']
      if event_id is not None:
	event = Event.objects.get(pk=event_id)
	form = EventForm(request.POST, instance=event)
      """
      form.save()
    else:
      form.error_list = ['need to get validation errors']
  else:
    if event_id is not None:
      event = Event.objects.get(pk=event_id)
      form = EventForm(instance=event)
    else:
      form = EventForm()
  form_fields = {'form':form,'event_id':event_id}
  form_fields.update(csrf(request))
  return render_to_response('gr/event_edit.html', form_fields)


