# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-24 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0016_rawleads_to_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawleads',
            name='to_delete',
            field=models.SmallIntegerField(default=0),
        ),
    ]