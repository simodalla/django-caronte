# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth import get_user_model
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.template import loader, Context
from django.utils.html import strip_tags

from allauth.exceptions import ImmediateHttpResponse

from ..models import LoginAuthorization, LogUnauthorizedLogin, AuthorizedDomain

User = get_user_model()


class AuthorizationService:

    def __init__(self, user=None):
        self._user = user

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def login_authorization(self):
        try:
            user = User.objects.get_by_natural_key(
                getattr(self.user, User.USERNAME_FIELD, ''))
        except User.DoesNotExist:
            raise LoginAuthorization.DoesNotExist()
        try:
            return LoginAuthorization.objects.get(user=user)
        except LoginAuthorization.DoesNotExist as exc:
            raise exc

    def make_unathorized_login(self, reason):
        try:
            LogUnauthorizedLogin.objects.create(
                username=self.user.get_username(), reason=reason)
        except Exception:
            pass
        return ImmediateHttpResponse(
            redirect(reverse('caronte:unauthorized_login')))

    def is_email_in_authorized_domain(self):
        email = self.user.email
        if not email or '@' not in email:
            return False
        domain = email.split('@')[1]
        try:
            AuthorizedDomain.objects.get(domain=domain)
            return True
        except AuthorizedDomain.DoesNotExist:
            return False

    def set_fields_from_authorized(self, authorized_user, fields=None):
        fields = fields or ['is_staff', 'is_superuser']
        for field in fields:
            setattr(self.user, field, getattr(authorized_user, field, False))

    def copy_fields(self, source_user, fields=None, dest_update=True):
        """
        Update fields from list param 'fields' to 'dest_user' User from
        'source_user' User.
        """
        fields = fields or []
        changed = False
        for field in fields:
            social_field = getattr(source_user, field)
            if not (getattr(self.user, field) == social_field):
                setattr(self.user, field, social_field)
                changed = True
        if changed and dest_update:
            self.user.save()
        return changed

    @staticmethod
    def _email_for_sociallogin(subject, template, context=None):
        context = context or {}
        message = loader.get_template(template).render(Context(context))
        mail_admins(subject,
                    strip_tags(message).lstrip('\n'),
                    fail_silently=True,
                    html_message=message)

    def email_new_sociallogin(self, request):
        email = self.user.email
        context = {'email': email,
                   'user_url': request.build_absolute_uri(
                       reverse(admin_urlname(self.user._meta, 'changelist')))
                               + '?email={}'.format(email)}
        subject = 'Nuovo socialaccount di {}'.format(email)
        return self._email_for_sociallogin(
            subject, "custom_email_user/email/new_sociallogin.html", context)

    def email_link_sociallogin(self, request):
        email = self.user.email
        context = {'email': email,
                   'user_url': request.build_absolute_uri(
                       self.user.get_absolute_url())}
        subject = 'Collegamento socialaccount di {}'.format(email)
        return self._email_for_sociallogin(
            subject, "custom_email_user/email/link_sociallogin.html", context)