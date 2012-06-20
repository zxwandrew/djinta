from django.conf.urls import patterns, url

urlpatterns = patterns('drawings.views',
    url(r'^$', 'index'),
    url(r'^(?P<drawing_id>\d+)/$', 'detail'),
    url(r'^create', 'create')
    )