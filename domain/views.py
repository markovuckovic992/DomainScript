from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib import unquote
from domain.models import RawLeads, Offer, BlackList, Log
from basic_editing import main_filter
from whois_domain import main, main_status
from django.core.mail import send_mail
from django.conf import settings
from django.db import connection
from datetime import datetime
from math import ceil
from os import popen
from operator import attrgetter 
import requests, hashlib, traceback, json

# EDITING
def editing(request):
    return render(request, 'editing.html', {})

def runEditing(request):
    try:
        path = settings.BASE_DIR
        com = request.POST['com'].replace('C:\\fakepath\\', '')
        net = request.POST['net'].replace('C:\\fakepath\\', '')
        org = request.POST['org'].replace('C:\\fakepath\\', '')
        info = request.POST['info'].replace('C:\\fakepath\\', '')
        redempt = request.POST['redempt'].replace('C:\\fakepath\\', '')
        date = request.POST['date']
        date = datetime.strptime(date, '%d-%m-%Y').date()
        RawLeads.objects.filter(date=date).delete()
        argument = "pypy " + path + "/basic_editing.py "
        argument += (com + " " + net + " " + org + " " + info + " ")
        argument += (redempt + " " + str(date))
        popen(argument)
        # main_filter(com, net, org, info, redempt, date)
        blacklist = BlackList.objects.all()
        for item in blacklist:
            RawLeads.objects.filter(name_zone=item.lead).delete()
        return HttpResponse('{"status": "success"}', content_type="application/json")
    except:
        print traceback.format_exc(), argument
        return HttpResponse('{"status": "failed"}', content_type="application/json")

# RAW LEADS
def rawLeads(request):
    if 'date' in request.GET.keys():
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()
    raw_leads = RawLeads.objects.filter(date=date, activated=0)
    try:
        log = Log.objects.get(date=date)
    except Log.DoesNotExist:
        log = None
    return render(
        request,
        'raw_leads.html',
        {
            "raw_leads": raw_leads,
            'range': range(1, int(ceil(len(raw_leads) / 5000)) + 2),
            'log': log,
            'total_r': len(raw_leads),
            'total_a': len(RawLeads.objects.filter(date=date, activated=1)),
        })

def reverse_state(request):
    raw_leads_id = int(unquote(request.POST['id']))
    mark = RawLeads.objects.get(id=raw_leads_id).mark
    mark += 1
    mark %= 2
    RawLeads.objects.filter(id=raw_leads_id).update(mark=mark)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def select_all(request):
    page = request.POST['page']
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(page=page, date=date)
    raw_leads.update(mark=1)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def add_this_name(request):
    redemption = request.POST['redemption']
    page = request.POST['page']
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(name_redemption=redemption, page=page, date=date)
    raw_leads.update(mark=1)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def find_mails(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    main(date)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def truncate(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(activated=0, date=date)
    raw_leads.delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")

# ACTIVE LEADS
def activeLeads(request):
    if 'date' in request.GET.keys():
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()
    raw_leads = RawLeads.objects.filter(activated=1, date=date)
    try:
        log = Log.objects.get(date=date)
    except Log.DoesNotExist:
        log = None
    return render(
        request,
        'active_leads.html',
        {
            "raw_leads": raw_leads,
            'range': range(1, int(ceil(len(raw_leads) / 5000)) + 2),
            'log': log,
            'total_r': len(RawLeads.objects.filter(activated=0, date=date)),
            'total_a': len(raw_leads),
        })

def blacklist(request):
    leads_id = int(unquote(request.POST['id']))
    blacklist = RawLeads.objects.get(id=leads_id).blacklist
    blacklist += 1
    blacklist %= 2
    RawLeads.objects.filter(id=leads_id).update(blacklist=blacklist)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def delete(request):
    leads_id = int(unquote(request.POST['id']))
    to_delete = RawLeads.objects.get(id=leads_id).to_delete
    to_delete += 1
    to_delete %= 2
    RawLeads.objects.filter(id=leads_id).update(to_delete=to_delete)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def mark_to_send(request):
    leads_id = int(unquote(request.POST['id']))
    mark_to_send = RawLeads.objects.get(id=leads_id).mark_to_send
    mark_to_send += 1
    mark_to_send %= 2
    RawLeads.objects.filter(id=leads_id).update(mark_to_send=mark_to_send)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def add_mail_man(request):
    mail = request.POST['email']
    lead_id = request.POST['id']
    name_zone = RawLeads.objects.get(id=lead_id).name_zone
    RawLeads.objects.filter(name_zone=name_zone).update(mail=mail)
    ids = map(attrgetter('id'), RawLeads.objects.filter(name_zone=name_zone))
    response = {
        'ids': ids,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

def rem_mail(request):
    lead_id = request.POST['id']
    name_zone = RawLeads.objects.get(id=lead_id).name_zone
    RawLeads.objects.filter(name_zone=name_zone).update(mail=None)
    ids = map(attrgetter('id'), RawLeads.objects.filter(name_zone=name_zone))
    response = {
        'ids': ids,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

def send_mails(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    delete = RawLeads.objects.filter(to_delete=1).delete()
    blacklists = RawLeads.objects.filter(blacklist=1)
    for blacklist in blacklists:
        entry = BlackList.objects.filter(lead=blacklist.name_zone)
        if not entry.exists():
            new = BlackList(lead=blacklist.name_zone)
            new.save()
    RawLeads.objects.filter(blacklist=1).delete()
    potential_profits = RawLeads.objects.filter(date=date, mark_to_send=1)
    for potential_profit in potential_profits:
        # Form a link
        hash = hashlib.md5()
        hash.update(str(potential_profit.id))
        hash_base_id = hash.hexdigest()
        link = ('http://www.webdomainexpert.pw/offer/?id=' + str(hash_base_id))
        try:
            send_mail(
                "Domain offer",  # Title
                potential_profit.name_zone,  # Body
                settings.EMAIL_HOST_USER,
                [potential_profit.mail],
                fail_silently=True,
                html_message="<a href='" + str(link) + "'>Link</a>",
            )

            requests.post(
                "http://www.webdomainexpert.pw/add_offer/",
                data={
                    'base_id': potential_profit.id,
                    'drop': potential_profit.name_redemption,
                    'lead': potential_profit.name_zone,
                    'hash_base_id': hash_base_id,
                }
            )

            # offer = Offer(
            #     base_id=potential_profit.id,
            #     lead=potential_profit.name_redemption,
            #     zone=potential_profit.name_zone,
            #     hash_base_id=hash_base_id
            # )
            # offer.save()

            RawLeads.objects.filter(id=potential_profit.id).delete()
        except:
            print traceback.format_exc()
    return HttpResponse('{"status": "success"}', content_type="application/json")
