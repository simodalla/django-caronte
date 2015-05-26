# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse


class AccountsLoginRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:index')


class AccountsLogoutRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:logout')


class AccountsPasswordChangeView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:password_change')


class AccountsInactiveRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:index')


class AdminPasswordResetRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('account_reset_password')


class UnauthorizedLogin(TemplateView):

    template_name = 'caronte/unauthorized_login.html'
