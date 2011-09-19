# IMM4LFO 2011-09-16
#

from django.conf.urls.defaults import *

urlpatterns = patterns('gr.views',
    (r'^$', 'index'),

    (r'^event/$', 'event_list'),
    (r'^event/add/$', 'event_edit'),
    (r'^event/edit/(?P<event_id>\d+)/$', 'event_edit'),
    (r'^event/edit/(?P<event_id>\d+)/(?P<remove_flag>del)/$', 'event_edit'),

    (r'^wishlist/$', 'wishlist_index'),
    (r'^wishlist/(?P<user_id>\d+)/$', 'wishlist_list'),
    (r'^wishlist/(?P<user_id>\d+)/add/$', 'wishlist_edit'),
    (r'^wishlist/(?P<user_id>\d+)/edit/(?P<wishlist_id>\d+)/$', 'wishlist_edit'),

    #(r'^(?P<pk>\d+)/$', 'ummmm'),
)
