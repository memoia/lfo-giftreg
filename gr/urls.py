# IMM4LFO 2011-09-16
#

from django.conf.urls.defaults import *

urlpatterns = patterns('gr.views',
    (r'^$', 'index'),

    (r'^event/$', 'event_list'),
    (r'^event/add/$', 'event_edit'),
    (r'^event/edit/(?P<event_id>\d+)/$', 'event_edit'),
    (r'^event/edit/(?P<event_id>\d+)/(?P<remove_flag>del)/$', 'event_edit'),
    (r'^event/view/(?P<event_id>\d+)/$', 'event_view'),

    (r'^wishlist/$', 'wishlist_index'),
    (r'^wishlist/(?P<user_id>\d+)/$', 'wishlist_list'),
    (r'^wishlist/(?P<user_id>\d+)/add/$', 'wishlist_edit'),
    (r'^wishlist/(?P<user_id>\d+)/edit/(?P<wishlist_id>\d+)/$', 'wishlist_edit'),

    (r'^attendee/(?P<attendee_id>\d+)/budget/(?P<event_id>\d+)/$', 'attendee_budget_edit'),

    (r'^attendee/(?P<attendee_id>\d+)/gifts/(?P<event_id>\d+)/$', 'attendee_gifts_list'),

    (r'^auth/register/$', 'auth_register'),
    (r'^auth/login/$', 'auth_login'),
    (r'^auth/logout/$', 'auth_logout'),

    #(r'^(?P<pk>\d+)/$', 'ummmm'),
)
