from django.conf.urls import url
from . import views

#app_name = 'blog' 如果这里不定义app_name，那么url里面就需要定义namespace
urlpatterns = [
	#url(r'^$', views.index, name='index'),
	url(r'^$',views.IndexView.as_view(), name='index'),
	url(r'^post/(?P<pk>[0-9]+)/$',views.detail, name='detail'),
	url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
	#url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
	url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
]
