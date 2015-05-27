# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizedDomain',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('domain', models.CharField(unique=True, max_length=254, verbose_name='domain')),
            ],
            options={
                'verbose_name_plural': 'authorized domains',
                'verbose_name': 'authorized domain',
            },
        ),
        migrations.CreateModel(
            name='LoginAuthorization',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('username', models.CharField(unique=True, max_length=254)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('is_denied', models.BooleanField(help_text='Designates that this user is denied to login.', default=False, verbose_name='deny status')),
            ],
            options={
                'verbose_name_plural': 'authorized users',
                'verbose_name': 'authorized user',
            },
        ),
        migrations.CreateModel(
            name='LogUnauthorizedLogin',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
