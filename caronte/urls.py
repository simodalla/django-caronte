# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^login/$',  views.AccountsLoginRedirectView.as_view()),
    url(r'^logout/$', views.AccountsLogoutRedirectView.as_view()),
    url(r'^password/change/$', views.AccountsPasswordChangeView.as_view()),
    url(r'^inactive/$', views.AccountsInactiveRedirectView.as_view()),
    url(r'^unauthorizedlogin/$', views.UnauthorizedLogin.as_view(),
        name='unauthorized_login'),
)
