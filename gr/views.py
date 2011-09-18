# IMM4LFO 2011-09-16
#

from django.shortcuts import render_to_response, get_object_or_404
from gr.models import Event


def index(request):
  return render_to_response('gr/main.html', {})

