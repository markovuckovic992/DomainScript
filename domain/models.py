from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

class RawLeads(models.Model):
    name_zone = models.CharField(max_length=100)
    name_redemption = models.CharField(max_length=100)
    mail = models.CharField(max_length=100, blank=True, null=True)

    sent = models.SmallIntegerField(default=0)
    archive = models.SmallIntegerField(default=0)
    send_mail = models.SmallIntegerField(default=0)
    to_archive = models.SmallIntegerField(default=0)
    to_delete = models.SmallIntegerField(default=0)
    return_or_delete = models.SmallIntegerField(default=0)

    blacklist = models.SmallIntegerField(default=0)
    mark_to_send = models.SmallIntegerField(default=0)

    date = models.DateField(default=timezone.now)

    class Meta:
        db_table = "raw_leads"


class Offer(models.Model):
    lead = models.CharField(max_length=100)
    zone = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    base_id = models.IntegerField()
    hash_base_id = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    response = models.SmallIntegerField(default=0)

    date = models.DateField(default=timezone.now)
    date_resp = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'ponude'
