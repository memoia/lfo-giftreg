# IMM4LFO 2011-09-16
#

from django.shortcuts import render_to_response, get_object_or_404, redirect
#from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.db.models import F, Q
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

def event_view(request, event_id):
  try:
    event = Event.objects.select_related(depth=1).get(pk=event_id)
  except Event.DoesNotExist:
    return redirect(event_list)
  return render_to_response('gr/event_view.html', {'event':event, 'user':request.user})

def event_edit(request, event_id=None, remove_flag=None):
  if remove_flag == 'del' and event_id is not None:
    # XXX should check that user deleting it is the associated rcp
    Event.objects.get(pk=event_id).delete()
    return redirect(event_list) #HttpResponseRedirect(reverse(event_list))

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
      return redirect(event_list) #HttpResponseRedirect(reverse(event_list))

  else:
    if event_id is not None:
      try:
	event = Event.objects.get(pk=event_id)
      except Event.DoesNotExist:
	return redirect(event_list)
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
    return redirect(wishlist_index)

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
      wl.recipient= User.objects.get(pk=form.cleaned_data['wishlist_recipient'])
      wl.gift = gi
      wl.active = form.cleaned_data['wishlist_active']
      wl.save()
      return redirect(wishlist_list,user_id=user_id)

  else:
    if wishlist_id is not None:
      w = RecipientWishList.objects.select_related(depth=1).get(pk=wishlist_id)
      if str(w.recipient.id) != str(user_id):
	return redirect(wishlist_list,user_id=user_id)
      ws = {
	  'wishlist_recipient': w.recipient.id
	, 'gift_name':		w.gift.name
	, 'gift_value':		w.gift.value
	, 'gift_id':		w.gift.id
	, 'wishlist_active':	w.active
	, 'wishlist_id':	w.id
      }
      form = RecipientWishListWithGiftForm(initial=ws)
    else:
      form=RecipientWishListWithGiftForm(initial={'wishlist_recipient':user_id})

  form_fields = {'form':form,'user_id':user_id}
  form_fields.update(csrf(request))
  return render_to_response('gr/wishlist_edit.html', form_fields)





def attendee_budget_edit(request, attendee_id, event_id):

  # ensure a budget can't be modified for an attendee
  # who isn't invited to the specified event (only if
  # sessions are working to make quick checks easier...)
  if request.user.id is not None:
    try:
      t=Event.objects.get(id__exact=event_id, attendees__id__exact=attendee_id)
    except Event.DoesNotExist:
      return redirect(event_view, event_id=event_id)

  def _get_budget(event_id, attendee_id):
    return AttendeeBudget.objects.get( \
			event__exact=event_id, attendee__exact=attendee_id)

  if request.method == 'POST':
    form = AttendeeBudgetForm(request.POST)
    if form.is_valid():
      e = form.cleaned_data['event']
      a = form.cleaned_data['attendee']
      try:
	b = _get_budget(e,a)
      except AttendeeBudget.DoesNotExist:
	b = AttendeeBudget()
	b.event = Event.objects.get(pk=e)
	b.attendee = User.objects.get(pk=a)
      b.maxpurchases = form.cleaned_data['maxpurchases']
      b.save()
      return redirect(event_view, event_id=e) 
    else:
      form_fields = {'form':form}
      form_fields.update(csrf(request))
      return render_to_response('gr/attendee_budget_edit.html', form_fields)

  else:
    d = {'attendee':attendee_id,'event':event_id}
    try:
      budget = _get_budget(event_id, attendee_id)
      d['maxpurchases'] = budget.maxpurchases
    except AttendeeBudget.DoesNotExist:
      pass
    form = AttendeeBudgetForm(initial=d)
    form_fields = {'form':form}
    form_fields.update(csrf(request))
    return render_to_response('gr/attendee_budget_edit.html', form_fields)



def attendee_gifts_list(request, attendee_id, event_id):

  # I hope there's a better way to do this....
  event = Event.objects.get(pk=1)
  recipient = User.objects.get(pk=event.recipient.id)
  wishlist = RecipientWishList.objects \
	      .filter(recipient=recipient) \
	      .select_related(depth=1) \
	      .exclude(gift__in= \
		AttendeeGifts.objects.filter( \
		  Q(event__id=event_id), \
		  ~Q(attendee__id=attendee_id) \
		) \
	      )

  gifts = Gift.objects.filter(pk__in=[w.gift.id for w in wishlist])

  form = AttendeeGiftsForm(queryset=gifts)
  form_fields = {'form':form}
  form_fields.update(csrf(request))
  return render_to_response('gr/attendee_gifts_list.html', form_fields)









