# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-02 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0010_auto_20170527_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='date',
            field=models.CharField(default='none', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='setting',
            name='run',
            field=models.SmallIntegerField(default=0),
        ),
    ]
