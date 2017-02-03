from django.conf.urls import url
# from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^user/(?P<user_id>\d+)$', views.user),
    url(r'^logout$', views.logout),
    url(r'^quote/create$', views.create),
    url(r'^quotes$', views.quotes),
    url(r'^favorite/add/(?P<quoteid>\d+)$', views.addFavorite),
    url(r'^favorite/destroy/(?P<favoriteid>\d+)$', views.destroyFavorite),
]
