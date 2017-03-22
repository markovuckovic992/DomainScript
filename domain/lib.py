from django.db import models
from domain.models import *
from datetime import datetime, timedelta

def removeStuff():
    date = datetime.now().date() - timedelta(days=27)
    RawLeads.objects.filter(date__lt=date).delete()
    # # blacklisting
    bads = BlackList.objects.all()
    for bad in bads:
        bad2 = "".join(bad.email.split())
        regex = r"\s*" + str(bad2) + "\s*"
        datas = RawLeads.objects.filter(mail__regex=regex)
        for data in datas:
            record = DeletedInfo(
                name_zone=data.name_zone,
                name_redemption=data.name_redemption,
                date=data.date,
                email=data.mail,
                reason='email is blacklisted'
            )
            record.save()
            RawLeads.objects.filter(id=data.id).delete()

    sbads = SuperBlacklist.objects.all()
    for sbad in sbads:
        bad2 = "".join(sbad.domain.split())
        bad2 = '@' + bad2
        datas = RawLeads.objects.filter(mail__icontains=bad2)
        for data in datas:
            record = DeletedInfo(
                name_zone=data.name_zone,
                name_redemption=data.name_redemption,
                date=data.date,
                email=data.mail,
                reason='domain is blacklisted'
            )
            record.save()
            RawLeads.objects.filter(id=data.id).delete()
    # # end blacklist #

    # # delete duplicates
    unique_fields = ['name_redemption', 'mail']
    duplicates = (RawLeads.objects.values(*unique_fields).order_by().annotate(max_id=models.Max('id'), count_id=models.Count('id')).filter(count_id__gt=1, activated=1, mail__isnull=False))

    for duplicate in duplicates:
        datas = (RawLeads.objects.filter(**{x: duplicate[x] for x in unique_fields}).exclude(id=duplicate['max_id']))
        for data in datas:
            record = DeletedInfo(
                name_zone=data.name_zone,
                name_redemption=data.name_redemption,
                date=data.date,
                email=data.mail,
                reason='duplicate'
            )
            record.save()
            RawLeads.objects.filter(id=data.id).delete()
    # # end delete #
    return 1
