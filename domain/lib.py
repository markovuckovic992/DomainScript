from django.db import models
from domain.models import *

def removeStuff():
    # # blacklisting
    bads = BlackList.objects.all()
    for bad in bads:
        bad2 = "".join(bad.email.split())
        regex = r"\s*" + str(bad2) + "\s*"
        RawLeads.objects.filter(mail__regex=regex).delete()

    sbads = SuperBlacklist.objects.all()
    for sbad in sbads:
        bad2 = "".join(sbad.domain.split())
        bad2 = '@' + bad2
        RawLeads.objects.filter(mail__icontains=bad2).delete()
    # # end blacklist #

    # # delete duplicates
    unique_fields = ['name_redemption', 'mail']
    duplicates = (RawLeads.objects.values(*unique_fields).order_by().annotate(max_id=models.Max('id'), count_id=models.Count('id')).filter(count_id__gt=1, activated=1, mail__isnull=False))

    for duplicate in duplicates:
        (RawLeads.objects.filter(**{x: duplicate[x] for x in unique_fields}).exclude(id=duplicate['max_id']).delete())
    # # end delete #
    return 1