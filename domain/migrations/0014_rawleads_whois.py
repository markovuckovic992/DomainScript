# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-10 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0013_rawleads_list_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawleads',
            name='whois',
            field=models.SmallIntegerField(default=0),
        ),
    ]
