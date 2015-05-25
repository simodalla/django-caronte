# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AuthorizedDomain(models.Model):
    domain = models.CharField(_('domain'), max_length=254, unique=True)

    class Meta:
        verbose_name = _('authorized domain')
        verbose_name_plural = _('authorized domains')


class LoginAuthorization(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_superuser = models.BooleanField(
        _('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    is_denied = models.BooleanField(
        _('deny status'), default=False,
        help_text=_('Designates that this user is denied to login.'))

    class Meta:
        verbose_name = _('authorized user')
        verbose_name_plural = _('authorized users')


class LogUnauthorizedLogin(models.Model):
    UNAUTHORIZED_REASONS = (
        ('domain', _('Domain Unauthorized')),
        ('notactive', _('User Not Active')),
        ('deny', _('User Denied')),
    )

    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=254)
    reason = models.CharField(max_length=254, choices=UNAUTHORIZED_REASONS,
                              null=True)

    class Meta:
        verbose_name = _('log unauthorized login')
        verbose_name_plural = _('log unauthorized logins')
