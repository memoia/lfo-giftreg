# IMM4LFO 2011-09-16
#

from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Default app
    (r'^$', redirect_to, {'url':'/gr/'}),

    # Just for testing...
    (r'^public/(?P<path>.*)$', 'django.views.static.serve', \
            {'document_root': settings.PUBLIC_ROOT}),

    (r'^gr/', include('gr.urls')),

    (r'^admin/', include(admin.site.urls)),
)
