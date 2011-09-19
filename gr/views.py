# IMM4LFO 2011-09-16
#

from django.shortcuts import render_to_response, get_object_or_404
from datetime import datetime
from gr.models import *


def index(request):
  return render_to_response('gr/main.html', {})


def event_list(request):
  #events = Event.objects.all()	  # use objects.select_related()?
  events=Event.objects.filter(date__gte=datetime.now()).select_related(depth=1)
  return render_to_response('gr/event_list.html', {'events':events})

def event_view(request):
  pass

def event_edit(request):
  pass


