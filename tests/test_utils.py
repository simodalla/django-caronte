# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import pytest

from django.test import TestCase
from django.core.urlresolvers import reverse

from allauth.exceptions import ImmediateHttpResponse

from custom_email_user.models import EmailUser

from caronte.models import (LoginAuthorization, LogUnauthorizedLogin,
                            AuthorizedDomain)
from caronte.allauth.utils import AuthorizationService


class TestAuthorizationService(TestCase):

    def setUp(self):
        self.domain = 'example.com'
        self.email = 'demo@{}'.format(self.domain)
        self.user = EmailUser(email=self.email)
        self.service = AuthorizationService(user=self.user)

    def test_login_authorization_raise_exc_if_user_not_exist(self):
        with pytest.raises(LoginAuthorization.DoesNotExist) as exinfo:
            login = self.service.login_authorization
        self.assertEqual('', str(exinfo.value))

    def test_login_authorization_raise_exc_if_loginauthorization_not_exist(self):
        self.user.save()
        # LoginAuthorization.objects.create(user=self.user)
        with pytest.raises(LoginAuthorization.DoesNotExist) as exinfo:
            login_auth = self.service.login_authorization
        self.assertIn('LoginAuthorization matching query does not exist',
                      str(exinfo.value))

    def test_login_authorization_return_loginauthorization_obj(self):
        self.user.save()
        LoginAuthorization.objects.create(user=self.user)
        login_auth = self.service.login_authorization
        self.assertTrue(isinstance(login_auth, LoginAuthorization))

    def test_make_unathorized_login_create_log(self):
        self.service.make_unathorized_login('crash')
        log = LogUnauthorizedLogin.objects.first()
        self.assertEqual(log.username, self.user.email)
        self.assertEqual(log.reason, 'crash')

    def test_make_unathorized_login_return_immediatehttpresponse(self):
        result = self.service.make_unathorized_login('crash')
        self.assertTrue(isinstance(result, ImmediateHttpResponse))
        self.assertTrue(result.response['Location'],
                        reverse('caronte:unauthorized_login'))

    def test_is_email_return_false_without_user_email(self):
        self.user.email = None
        self.assertFalse(self.service.is_email_in_authorized_domain())

    def test_is_email_return_false_with_wrong_email(self):
        self.user.email = 'wrong'
        self.assertFalse(self.service.is_email_in_authorized_domain())

    def test_is_email_return_false_if_domain_is_not_authorized(self):
        self.assertFalse(self.service.is_email_in_authorized_domain())

    def test_is_email_return_true_if_domain_is_authorized(self):
        AuthorizedDomain.objects.create(domain=self.domain)
        self.assertTrue(self.service.is_email_in_authorized_domain())


