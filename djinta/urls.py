from django.conf.urls import patterns, include, url
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djinta.views.home', name='home'),
    # url(r'^djinta/', include('djinta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),   
    url(r'^drawings/', include('drawings.urls')),
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    (r'^charts/simple.png$', 'drawings.calc.simple'),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'tempfront/index.html'}),
    
    #(r'^$', 'django.views.generic.simple.direct_to_template', {'template': '/template/tempfront'}),

    #url(r'^$', 'drawings.views.create'),

)
