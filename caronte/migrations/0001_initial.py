# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('custom_email_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizedDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('domain', models.CharField(max_length=254, unique=True, verbose_name='domain')),
            ],
            options={
                'verbose_name_plural': 'authorized domains',
                'verbose_name': 'authorized domain',
            },
        ),
        migrations.CreateModel(
            name='LoginAuthorization',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('is_denied', models.BooleanField(verbose_name='deny status', help_text='Designates that this user is denied to login.', default=False)),
            ],
            options={
                'verbose_name_plural': 'authorized users',
                'verbose_name': 'authorized user',
            },
        ),
        migrations.CreateModel(
            name='LogUnauthorizedLogin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=254)),
                ('reason', models.CharField(null=True, max_length=254, choices=[('domain', 'Domain Unauthorized'), ('notactive', 'User Not Active'), ('deny', 'User Denied')])),
            ],
            options={
                'verbose_name_plural': 'log unauthorized logins',
                'verbose_name': 'log unauthorized login',
            },
        ),
    ]
