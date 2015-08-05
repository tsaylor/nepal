from django.conf.urls import include, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from groups.models import Group


urlpatterns = [
    url(r'^$', ListView.as_view(model=Group), name='group_list'),
    url(r'^(?P<slug>[-\w]+)/?$', DetailView.as_view(model=Group), name='group_detail'),
    #url(r'^create/?$', 'groups.views.auth_test', name='group_create'),
]
