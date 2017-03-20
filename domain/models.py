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
    no_email_found = models.SmallIntegerField(default=0)

    date = models.DateField(default=timezone.now)
    hash_base_id = models.CharField(max_length=32, unique=True, blank=True, null=True)
    reminder = models.SmallIntegerField(default=0)
    last_email_date = models.DateTimeField(default=timezone.now)

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
    number_act = models.IntegerField(default=0)
    number_act_2 = models.IntegerField(default=0)
    number_sent = models.IntegerField(default=0)
    number_sent_2 = models.IntegerField(default=0)

class BlackList(models.Model):
    email = models.CharField(max_length=320, blank=True, null=True)

    class Meta:
        db_table = 'blacklist'

class AllHash(models.Model):
    hash_base_id = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = 'hashes'

class Emails(models.Model):
    email = models.CharField(max_length=320, blank=True, null=True)
    name_zone = models.CharField(max_length=100)

    class Meta:
        db_table = 'emails'

class Setting(models.Model):
    number_of_days = models.IntegerField(default=5)
    com_net = models.SmallIntegerField(default=2)  # 0 com, 1 net, 2 both
    length = models.SmallIntegerField(default=60)
    number_of_digits = models.SmallIntegerField(default=0)
    number_of_keywords = models.SmallIntegerField(default=3)
    allow_bad_keywords = models.SmallIntegerField(default=1)
    min_length = models.SmallIntegerField(default=4)
    max_length = models.SmallIntegerField(default=11)

    class Meta:
        db_table = 'settings'

class ProcessTracker(models.Model):
    email = models.CharField(max_length=320, blank=True, null=True)
    name_redemption = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'process_tracker'

class DeletedInfo(models.Model):
    name_zone = models.CharField(max_length=100)
    name_redemption = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    email = models.CharField(max_length=320, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'delete_info'


class EventLogger(models.Model):
    ip = models.CharField(max_length=16)
    action = models.CharField(max_length=10000)
    date = models.DateTimeField(default=timezone.now)

class DomainException(models.Model):
    domain = models.CharField(max_length=60)
