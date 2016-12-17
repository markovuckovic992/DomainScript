from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

class RawLeads(models.Model):
    name_zone = models.CharField(max_length=100)
    name_redemption = models.CharField(max_length=100)
    mail = models.CharField(max_length=320, blank=True, null=True)
    page = models.SmallIntegerField(default=1)

    activated = models.SmallIntegerField(default=0)
    mark = models.SmallIntegerField(default=0)
    mark_to_send = models.SmallIntegerField(default=0)
    to_delete = models.SmallIntegerField(default=0)
    blacklist = models.SmallIntegerField(default=0)

    date = models.DateField(default=timezone.now)

    class Meta:
        db_table = "raw_leads"

class SuperBlacklist(models.Model):
    domain = models.CharField(max_length=100)

    class Meta:
        db_table = 'super_blacklist'

class Log(models.Model):
    date = models.DateField(default=timezone.now)
    number_of_redemption = models.IntegerField(default=0)
    number_of_all = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)

class BlackList(models.Model):
    email = models.CharField(max_length=320, blank=True, null=True)

    class Meta:
        db_table = 'blacklist'

class AllHash(models.Model):
    hash_base_id = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = 'hashes'
