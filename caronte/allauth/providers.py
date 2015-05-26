# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse

from ..models import LogUnauthorizedLogin, LoginAuthorization, AuthorizedDomain


User = get_user_model()


class AuthorizationSocialAccountAdapter(DefaultSocialAccountAdapter):

    @staticmethod
    def _response_user_is_denied_or_inactive(username, reason=None):
        try:
            LogUnauthorizedLogin.objects.create(
                username=username, reason=reason)
        except Exception:
            pass
        return ImmediateHttpResponse(redirect(
            reverse('caronte:unauthorized_login')))

    @staticmethod
    def _login_authorization(user):
        try:
            return LoginAuthorization.objects.get(user__email=user.email)
        except LoginAuthorization.DoesNotExist:
            return None

    @staticmethod
    def _is_in_authorized_domain(email):
        if '@' not in email:
            return False
        domain = email.split('@')[1]
        try:
            AuthorizedDomain.objects.get(domain=domain)
            return True
        except AuthorizedDomain.DoesNotExist:
            return False

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        # email = sociallogin.user.email
        # import ipdb
        # ipdb.set_trace()

        authorized_user = self._login_authorization(user)

        if authorized_user:
            if authorized_user.is_denied:
                # login of user denied
                raise self._response_user_is_denied_or_inactive(
                    user.email, 'deny')
        else:
            # login of domain not authorized
            if not self._is_in_authorized_domain(user.email):
                raise self._response_user_is_denied_or_inactive(
                    user.email, 'domain')
        print("*****************************************")
        try:
            local_user = User.objects.get(email=user.email)
            print(local_user)
            if not local_user.is_active:
                # login of user not active
                raise self._response_user_is_denied_or_inactive(
                    user.email, 'notactive')
            if not sociallogin.is_existing:  # sociallogin not exist
                User.objects.set_fields_from_authorized(local_user,
                                                        authorized_user)
                User.objects.copy_fields(local_user,
                                         sociallogin.account.user,
                                         ['last_name', 'first_name'],
                                         dest_update=True)
                sociallogin.account.user = local_user
                sociallogin.save(request)
                User.objects.email_link_sociallogin(request, sociallogin)
        except User.DoesNotExist:
            User.objects.set_fields_from_authorized(user, authorized_user)
            # sociallogin.account.user.set_fields_from_authorized(
            #     authorized_user)
            User.objects.email_new_sociallogin(request, user)


class AuthorizationAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return True
