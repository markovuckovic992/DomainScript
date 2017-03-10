# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-07 16:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0034_rawleads_last_email_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_zone', models.CharField(max_length=100)),
                ('name_redemption', models.CharField(max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('email', models.CharField(blank=True, max_length=320, null=True)),
                ('reason', models.CharField(blank=True, max_length=320, null=True)),
            ],
            options={
                'db_table': 'delete_info',
            },
        ),
    ]