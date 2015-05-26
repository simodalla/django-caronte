# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    url("^admin/", include(admin.site.urls)),
    url(r'^accounts/', include('caronte.urls', namespace='caronte')),
]
