# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-20 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0038_auto_20170315_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainException',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=60)),
            ],
        ),
    ]
