# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-26 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0004_whoisanalytics'),
    ]

    operations = [
        migrations.AddField(
            model_name='whoisanalytics',
            name='source',
            field=models.CharField(default='internal', max_length=8),
            preserve_default=False,
        ),
    ]
