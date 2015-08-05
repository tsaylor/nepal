from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.flatpages import views
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),  # noqa
    url(r'^auth-test', 'nepal.views.auth_test', name='auth-test'),
    url(r'^twitter/', include('twython_auth.urls')),
    url(r'^groups/', include('groups.urls')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^join/$', TemplateView.as_view(template_name="home.html"), name='join'),
)
