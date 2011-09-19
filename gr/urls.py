# IMM4LFO 2011-09-16
#

from django.conf.urls.defaults import *

urlpatterns = patterns('gr.views',
    (r'^$', 'index'),
    (r'^event/$', 'event_list'),
    (r'^event/add/$', 'event_edit'),
    (r'^event/edit/(?P<event_id>\d+)/$', 'event_edit'),
    (r'^(?P<pk>\d+)/$', 'ummmm'),
)
