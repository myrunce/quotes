from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^quotes$', views.quotes),
    url(r'^login$', views.login),
    url(r'^contribute$', views.contribute),
    url(r'^favorite$', views.favorite),
    url(r'^users/(?P<user_id>\d+)$', views.users),
    url(r'^logout$', views.logout),
    url(r'^remove$', views.remove),
    
]