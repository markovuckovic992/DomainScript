# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-06 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0002_auto_20161106_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawleads',
            name='send_mail',
            field=models.SmallIntegerField(default=0),
        ),
    ]
