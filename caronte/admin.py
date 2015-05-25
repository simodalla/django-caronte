# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .models import (AuthorizedDomain, LoginAuthorization,
                     LogUnauthorizedLogin)


@admin.register(AuthorizedDomain)
class AuthorizedDomainAdmin(admin.ModelAdmin):
    list_display = ('domain',)


@admin.register(LoginAuthorization)
class AuthorizedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_denied', 'is_staff', 'is_superuser',)

    # grapelli autocomplete
    raw_id_fields = ('user',)
    autocomplete_lookup_fields = {
        'fk': ['user'],
    }


@admin.register(LogUnauthorizedLogin)
class LogUnauthorizedLoginAdmin(admin.ModelAdmin):
    list_display = ('username', 'reason', 'created', )
