# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-25 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0031_rawleads_no_email_found'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=320, null=True)),
                ('name_redemption', models.CharField(max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'process_tracker',
            },
        ),
    ]
