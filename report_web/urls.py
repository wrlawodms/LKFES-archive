from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.list, name='index'),
	url(r'^(?P<page>[0-9]+)/$', views.list, name='list'),
	url(r'^post/$', views.post, name='post'),
	url(r'^download/(?P<post_id>[0-9]+)/(?P<file_name>\w.{0,256})/$', views.download),
	url(r'^detail/(?P<post_id>[0-9]+)/$',views.report, name='report')
]


