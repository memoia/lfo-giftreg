# IMM4LFO 2011-09-16
#

from django.conf.urls.defaults import *

urlpatterns = patterns('gr.views',
    (r'^$', 'index'),
    (r'^event/$', 'event_list'),
    (r'^(?P<pk>\d+)/$', 'ummmm'),
)
