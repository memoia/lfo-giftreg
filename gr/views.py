# IMM4LFO 2011-09-16
#

from django.shortcuts import render_to_response, get_object_or_404, redirect
#from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.db.models import F, Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
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
  return render_to_response('gr/event_list.html', {'events':events}, context_instance=RequestContext(request))

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

  # TODO it would be nice to left-join the attendeegifts
  #	 table somehow so that we could show if an item
  #	 has been selected by an attendee.
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
      if b.maxpurchases > 0:
	b.save()
      else:
	try:
	  b.delete()
	except AssertionError:
	  pass
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
  event = Event.objects.get(pk=event_id)
  wishlist = RecipientWishList.objects.attendee_options( \
		      event.recipient.id, attendee_id, event_id)

  gifts = Gift.objects.filter(pk__in=[w.gift.id for w in wishlist])

  prev_selected = AttendeeGifts.objects.filter(event__id=event_id, \
					    attendee__id=attendee_id)
  
  gift_choices = [ (x.id, x) for x in gifts ]
  gift_checked = [ x.gift.id for x in prev_selected ]

  try:
    budget = AttendeeBudget.objects.get(attendee__id=attendee_id, event=event).maxpurchases
  except AttendeeBudget.DoesNotExist:
    budget = None

  if request.method == 'POST':

    form = AttendeeGiftsForm(request.POST)
    form.fields['gifts'].choices = gift_choices
    if form.is_valid():
      prev_selected.delete()
      selected_gifts = request.POST.getlist('gifts')
      for g in selected_gifts:
	ag = AttendeeGifts()
	ag.attendee = User.objects.get(pk=attendee_id)
	ag.event = Event.objects.get(pk=event_id)
	ag.gift = Gift.objects.get(pk=g)
	ag.save()
      return redirect(event_view, event_id)
    else:
      form.fields['gifts'].choices = gift_choices
      form_fields = {
	  'form':form
	, 'budget':budget
	, 'attendee_id':attendee_id
	, 'event_id':event_id
      }
      form_fields.update(csrf(request))
      return render_to_response('gr/attendee_gifts_list.html', form_fields)

  form = AttendeeGiftsForm(initial={'event':event_id,'attendee':attendee_id})
  form.fields['gifts'].choices = gift_choices
  form.fields['gifts'].initial = gift_checked

  form_fields = {
      'form':form
    , 'budget':budget
    , 'attendee_id':attendee_id
    , 'event_id':event_id
  }
  form_fields.update(csrf(request))
  return render_to_response('gr/attendee_gifts_list.html', form_fields)



def auth_register(request):
  messages = []

  if request.method == 'POST':
    form = AuthRegisterForm(request.POST)
    if form.is_valid():
      uname = form.cleaned_data['email']
      passw = form.cleaned_data['password']
      utype = form.cleaned_data['user_type']

      u = None
      try:
	u = User.objects.get(username__iexact=uname)
      except User.DoesNotExist:
	pass

      if u:
	messages.append('A user with this name already exists')
      else:
	u = User.objects.create_user(uname,uname,passw)
	p = u.get_profile()
	p.gr_user_type = utype
	p.save()
	a = authenticate(username=uname,password=passw)
	login(request, a)
	return redirect(event_list)

  else:
    form = AuthRegisterForm()

  page_vars = {'form':form, 'messages':messages}
  page_vars.update(csrf(request))
  return render_to_response('gr/auth_register.html', page_vars)


def auth_login(request):
  messages = []

  if request.method == 'POST':
    form = AuthLoginForm(request.POST)
    if form.is_valid():
      u = authenticate(username=form.cleaned_data['username'], \
		       password=form.cleaned_data['password'] )
      if u is not None and u.is_active:
	login(request, u)
	return redirect(event_list)
      else:
	messages.append('Could not log in with supplied credentials.')

  else:
    form = AuthLoginForm()

  page_vars = {'form':form, 'messages':messages}
  page_vars.update(csrf(request))
  return render_to_response('gr/auth_login.html', page_vars)


def auth_logout(request):
  logout(request)
  return redirect(index)







