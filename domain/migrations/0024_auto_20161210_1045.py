# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-10 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0023_auto_20161205_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperBlacklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'super_blacklist',
            },
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
        migrations.RemoveField(
            model_name='blacklist',
            name='lead',
        ),
        migrations.AddField(
            model_name='blacklist',
            name='email',
            field=models.CharField(blank=True, max_length=320, null=True),
        ),
    ]
