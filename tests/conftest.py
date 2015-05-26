# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import pytest


@pytest.fixture()
def admin_user(db, django_user_model, django_username_field):
    """
    A Django admin EmailUser.

    This uses an existing user with username "admin@example.com", or creates
    a new one with password "password".
    """
    UserModel = django_user_model
    username_field = django_username_field
    email = 'admin@example.com'
    try:
        user = UserModel._default_manager.get(**{username_field: email})
    except UserModel.DoesNotExist:
        user = UserModel._default_manager.create_superuser(email, 'password')
    return user


@pytest.fixture()
def admin_client(db, admin_user):
    """
    A Django test client logged in as an admin EmailUser (via the
    ``admin_user`` fixture).
    """
    from django.test.client import Client

    client = Client()
    client.login(username=admin_user.email, password='password')
    return client


WINDOW_SIZE = (1024, 768)


@pytest.fixture(scope='session')
def display(request):
    try:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=WINDOW_SIZE)
        display.start()

        def fin():
            display.stop()

        request.addfinalizer(fin)
        return display
    except ImportError:
        print("Pyvirtualdisplay not installed!")
    except Exception as e:
        print("Error with pyvirtualdisplay.Display: {}".format(str(e)))
    return None


class LiveBrowser(object):

    def __init__(self, driver, live_server, user=None):
        length_implicitly_wait = 30
        self.driver = driver
        self.live_server = live_server
        self.driver.set_window_size(*WINDOW_SIZE)
        # if 'TRAVIS' in os.environ and os.environ['TRAVIS']:
        #     length_implicitly_wait = 20
        self.driver.implicitly_wait(length_implicitly_wait)
        self.user = user

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    def quit(self):
        self.driver.quit()

    @property
    def current_url(self):
        return self.driver.current_url.replace(self.live_server.url, '')

    def get(self, url, *args, **kwargs):
        from django.core.urlresolvers import reverse
        if url.startswith('/'):
            return self.driver.get('{}{}{}'.format(
                self.live_server.url,
                url.rstrip('/'),
                '/' if '?' not in url else ''), *args, **kwargs)
        return self.driver.get('{}{}'.format(
            self.live_server.url, reverse(url, args=args, kwargs=kwargs)))

    def create_pre_authenticated_session(self, user):
        from django.contrib.sessions.backends.db import SessionStore
        from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
        from django.conf import settings
        self.user = user
        session = SessionStore()
        session[SESSION_KEY] = self.user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # to set a cookie we need fo first visit the domain.
        # 404 pages load the quicktest! If is in testing of Mezzanine (>=3.1.9)
        # use an "admin" for bug on template_tags of mezzanine if app 'blog'
        # is not installed.
        self.driver.get(
            '{}/admin/404_no_such_url/'.format(self.live_server.url))
        self.driver.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))
        return session.session_key


@pytest.fixture
def browser(request, live_server):
    from selenium import webdriver
    driver = webdriver.Firefox()
    live_browser = LiveBrowser(driver, live_server)

    def fin():
        live_browser.quit()

    request.addfinalizer(fin)
    return live_browser


@pytest.fixture
def admin_browser(browser, admin_user):
    browser.create_pre_authenticated_session(admin_user)
    return browser
