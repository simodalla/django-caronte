# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse

from ..models import LogUnauthorizedLogin, LoginAuthorization, AuthorizedDomain
from .utils import AuthorizationService


User = get_user_model()


class AuthorizationSocialAccountAdapter(DefaultSocialAccountAdapter):

    # @staticmethod
    # def _response_user_is_denied_or_inactive(username, reason=None):
    #     try:
    #         LogUnauthorizedLogin.objects.create(
    #             username=username, reason=reason)
    #     except Exception:
    #         pass
    #     return ImmediateHttpResponse(redirect(
    #         reverse('caronte:unauthorized_login')))

    # @staticmethod
    # def _login_authorization(user):
    #     try:
    #         return LoginAuthorization.objects.get(user__email=user.email)
    #     except LoginAuthorization.DoesNotExist:
    #         return None

    # @staticmethod
    # def _is_in_authorized_domain(email):
    #     if '@' not in email:
    #         return False
    #     domain = email.split('@')[1]
    #     try:
    #         AuthorizedDomain.objects.get(domain=domain)
    #         return True
    #     except AuthorizedDomain.DoesNotExist:
    #         return False

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        service = AuthorizationService(user=user)
        try:
            authorized_user = service.login_authorization
        except LoginAuthorization.DoesNotExist:
            authorized_user = None

        if authorized_user:
            if authorized_user.is_denied:
                # login of user denied
                raise service.make_unathorized_login('deny')
        else:
            # login of domain not authorized
            if not service.is_email_in_authorized_domain():
                raise service.make_unathorized_login('domain')
        try:
            local_user = User.objects.get_by_natural_key(
                getattr(user, User.USERNAME_FIELD, ''))
            service.user = local_user
            if not local_user.is_active:
                # login of user not active
                raise service.make_unathorized_login('notactive')
            if not sociallogin.is_existing:  # sociallogin not exist
                # User.objects.set_fields_from_authorized(local_user,
                #                                         authorized_user)
                service.set_fields_from_authorized(authorized_user)
                # User.objects.copy_fields(local_user,
                #                          user,
                #                          ['last_name', 'first_name'],
                #                          dest_update=True)
                service.copy_fields(user, ['last_name', 'first_name'],
                                    dest_update=True)
                sociallogin.user = local_user
                sociallogin.save(request)
                # User.objects.email_link_sociallogin(request, sociallogin.user)
                service.email_link_sociallogin(request)
        except User.DoesNotExist:
            # User.objects.set_fields_from_authorized(user, authorized_user)
            service.set_fields_from_authorized(authorized_user)
            # User.objects.email_new_sociallogin(request, user)
            service.email_new_sociallogin(request)
