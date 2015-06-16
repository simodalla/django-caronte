# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import views

urlpatterns = [
    url(r'^unauthorizedlogin/$', views.UnauthorizedLogin.as_view(),
        name='unauthorized_login')
]
