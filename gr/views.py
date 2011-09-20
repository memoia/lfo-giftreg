# IMM4LFO 2011-09-16
#

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
import datetime
from gr.models import *
from gr.forms import *

"""
from django.core.mail import send_mail
send_mail(subject, message, sender, recipients)
"""


def index(request):
  return render_to_response('gr/main.html', {})


def event_list(request):
  events=Event.objects.filter(date__gte=datetime.datetime.now()) \
					    .select_related(depth=1)
  return render_to_response('gr/event_list.html', {'events':events})

def event_view(request):
  pass


def event_edit(request, event_id=None, remove_flag=None):
  if remove_flag == 'del' and event_id is not None:
    # XXX should check that user deleting it is the associated rcp
    Event.objects.get(pk=event_id).delete()
    return HttpResponseRedirect(reverse(event_list))

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
      return HttpResponseRedirect(reverse(event_list))
  else:
    if event_id is not None:
      event = Event.objects.get(pk=event_id)
      form = EventForm(instance=event)
    else:
      form = EventForm()
  form_fields = {'form':form,'event_id':event_id}
  form_fields.update(csrf(request))
  return render_to_response('gr/event_edit.html', form_fields)





def wishlist_index(request):
  wishlists=RecipientWishList.objects \
		  .values('recipient') \
		  .distinct()
  return render_to_response('gr/wishlist_index.html', {'wishlists':wishlists})

def wishlist_list(request, user_id=None):
  try:
    u = User.objects.get(pk=user_id)
  except User.DoesNotExist:
    # XXX broken
    return HttpResponseRedirect(reverse(wishlist_index))

  wlist = RecipientWishList.objects.filter(recipient=u).select_related(depth=1)
  return render_to_response('gr/wishlist_list.html', {'wlist':wlist, 'user':u})

def wishlist_edit(request, user_id, wishlist_id=None):
  if request.method == 'POST':
    form = RecipientWishListWithGiftForm(request.POST)
    if form.is_valid():
      try:    gi = Gift.objects.get(pk=form.cleaned_data['gift_id'])
      except: gi = Gift()

      try:    wl = RecipientWishList.objects \
			  .get(pk=form.cleaned_data['wishlist_id'])
      except: wl = RecipientWishList()

      #XXX this belongs as a transaction...
      gi.name = form.cleaned_data['gift_name']
      gi.value = form.cleaned_data['gift_value']
      gi.save()
      wl.recipient = User.objects.get(pk=form.cleaned_data['wishlist_recipient'])
      wl.gift = gi
      wl.active = form.cleaned_data['wishlist_active']
      wl.save()
      # XXX broken
      return HttpResponseRedirect(reverse(wishlist_list))

  else:
    if wishlist_id is not None:
      w = RecipientWishList.objects.select_related(depth=1).get(pk=wishlist_id)
      ws = {
	  'wishlist_recipient': w.id
	, 'gift_name': w.gift.name
	, 'gift_value': w.gift.value
	, 'gift_id':    w.gift.id
	, 'wishlist_active': w.active
	, 'wishlist_id': w.id
      }
      form = RecipientWishListWithGiftForm(initial=ws)
    else:
      form=RecipientWishListWithGiftForm(initial={'wishlist_recipient':user_id})

  form_fields = {'form':form,'user_id':user_id}
  form_fields.update(csrf(request))
  return render_to_response('gr/wishlist_edit.html', form_fields)





