# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from ..models import LoginAuthorization
from .utils import AuthorizationService


User = get_user_model()


class AuthorizationSocialAccountAdapter(DefaultSocialAccountAdapter):

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
                service.set_fields_from_authorized(authorized_user)
                service.copy_fields(user, ['last_name', 'first_name'],
                                    dest_update=True)
                sociallogin.user = local_user
                sociallogin.save(request)
                service.email_link_sociallogin(request)
        except User.DoesNotExist:
            service.set_fields_from_authorized(authorized_user)
            service.email_new_sociallogin(request)
