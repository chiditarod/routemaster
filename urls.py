from django.conf.urls.defaults import *

from routemaster.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Site Root
    #(r'^$', homepage),

    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    (r'^current_time/$', current_datetime),

    # (r'^routemaster/', include('routemaster.foo.urls')),
    (r'^hello/', hello),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
