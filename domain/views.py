from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib import unquote
from domain.models import *
from domain.apps import *
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
from random import randint


# EDITING
def editing(request):
    return render(request, 'editing.html', {})


def runEditing(request):
    try:
        path = settings.BASE_DIR
        arg = request.POST['arg']
        if int(arg) == 1:
            script = '_basic_editing'
        else:
            script = 'basic_editing'
        com = request.POST['com'].replace('C:\\fakepath\\', '')
        net = request.POST['net'].replace('C:\\fakepath\\', '')
        org = request.POST['org'].replace('C:\\fakepath\\', '')
        info = request.POST['info'].replace('C:\\fakepath\\', '')
        redempt = request.POST['redempt'].replace('C:\\fakepath\\', '')
        date = request.POST['date']
        date = datetime.strptime(date, '%d-%m-%Y').date()
        RawLeads.objects.filter(date=date).delete()
        argument = "pypy " + path + "/" + script + ".py "
        argument += (com + " " + net + " " + org + " " + info + " ")
        argument += (redempt + " " + str(date))
        popen(argument)
        # main_filter(com, net, org, info, redempt, date)
        return HttpResponse('{"status": "success"}', content_type="application/json")
    except:
        print traceback.format_exc(), argument
        return HttpResponse('{"status": "failed"}', content_type="application/json")


# RAW LEADS
def rawLeads(request):
    if 'date' in request.GET.keys() and len(request.GET['date']) > 6:
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()
    if 'page' in request.GET.keys():
        page = int(request.GET['page'])
    else:
        page = 1
    raw_leads = RawLeads.objects.filter(date=date, activated=0, page=page)
    numbers = [1]
    numbers += map(attrgetter('page'), RawLeads.objects.filter(date=date))
    number_of_pages = max(set(numbers))
    try:
        log = Log.objects.get(date=date)
    except Log.DoesNotExist:
        log = None
    return render(
        request,
        'raw_leads.html',
        {
            "raw_leads": raw_leads,
            'range': range(1, number_of_pages + 1),
            'log': log,
            'total_r': len(RawLeads.objects.filter(date=date, activated=0)),
            'total_a': len(RawLeads.objects.filter(date=date, activated=1)),
            'page': page,
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


def rem_this_name(request):
    redemption = request.POST['redemption']
    page = request.POST['page']
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(name_redemption=redemption, page=page, date=date)
    raw_leads.update(mark=0)
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
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    blacklist = RawLeads.objects.get(id=leads_id).blacklist
    blacklist += 1
    blacklist %= 2
    mail = RawLeads.objects.get(id=leads_id).mail
    RawLeads.objects.filter(mail=mail, activated=1, date=date).update(blacklist=blacklist)
    ids = map(attrgetter('id'), RawLeads.objects.filter(mail=mail, activated=1, date=date))
    response = {
        'ids': ids,
        'command': True if blacklist else False
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


def blacklist_selected(request):
    blacklists = RawLeads.objects.filter(blacklist=1)
    for blacklist in blacklists:
        entry = BlackList.objects.filter(email=blacklist.mail)
        if not entry.exists():
            new = BlackList(email=blacklist.mail)
            new.save()
    RawLeads.objects.filter(blacklist=1).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")


def delete(request):
    leads_id = int(unquote(request.POST['id']))
    to_delete = RawLeads.objects.get(id=leads_id).to_delete
    to_delete += 1
    to_delete %= 2
    RawLeads.objects.filter(id=leads_id).update(to_delete=to_delete)
    return HttpResponse('{"status": "success"}', content_type="application/json")


def mark_to_send(request):
    if 'id' in request.POST.keys():
        leads_id = int(unquote(request.POST['id']))
        mark_to_send = RawLeads.objects.get(id=leads_id).mark_to_send
        mark_to_send += 1
        mark_to_send %= 2
        RawLeads.objects.filter(id=leads_id).update(mark_to_send=mark_to_send)
    else:
        date = request.POST['date']
        date = datetime.strptime(date, '%d-%m-%Y').date()
        RawLeads.objects.filter(date=date).update(mark_to_send=1)
    return HttpResponse('{"status": "success"}', content_type="application/json")


def un_mark_to_send(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    RawLeads.objects.filter(date=date).update(mark_to_send=0)
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
        entry = BlackList.objects.filter(email=blacklist.mail)
        if not entry.exists():
            new = BlackList(email=blacklist.mail)
            new.save()
    RawLeads.objects.filter(blacklist=1).delete()
    potential_profits = RawLeads.objects.filter(date=date, mark_to_send=1)
    for potential_profit in potential_profits:
        hash = hashlib.md5()
        hash.update(str(potential_profit.id))
        hash_base_id = hash.hexdigest()
        try:
            link = ('http://www.webdomainexpert.pw/offer/?id=' + str(hash_base_id))
            unsubscribe = ('http://www.webdomainexpert.pw/unsubscribe/?id=' + str(hash_base_id))
            case = randint(1, 4)
            msg = eval('form_a_msg' + str(case) + '("' + str(potential_profit.name_redemption) + '","' + str(
                link) + '","' + str(unsubscribe) + '")')
            send_mail(
                msg[0],  # Title
                potential_profit.name_zone,  # Body
                settings.EMAIL_HOST_USER,
                [potential_profit.mail],
                fail_silently=False,
                html_message=msg[1],
            )

            requests.post(
                "http://www.webdomainexpert.pw/add_offer/",
                data={
                    'base_id': potential_profit.id,
                    'drop': potential_profit.name_redemption,
                    'lead': potential_profit.name_zone,
                    'hash_base_id': hash_base_id,
                    'remail': potential_profit.mail,
                }
            )

            RawLeads.objects.filter(id=potential_profit.id).delete()
        except:
            print traceback.format_exc()
    return HttpResponse('{"status": "success"}', content_type="application/json")


def blacklisting(request):
    blacklist = BlackList.objects.all()
    superblacklist = SuperBlacklist.objects.all()
    return render(request, 'super_blacklist.html',
                  {
                      'blacklist': blacklist,
                      'superblacklist': superblacklist,
                  })


def super_blacklist(request):
    domain = request.POST['domain']
    entry = SuperBlacklist.objects.filter(domain=domain)
    if not entry.exists():
        new_entry = SuperBlacklist(domain=domain)
        new_entry.save()
    exclude_email = '@' + str(domain)
    RawLeads.objects.filter(mail__endswith=exclude_email).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")


def regular_blacklist(request):
    email = request.POST['email']
    entry = BlackList.objects.filter(email=email)
    if not entry.exists():
        new_entry = BlackList(email=email)
        new_entry.save()
    RawLeads.objects.filter(mail=email).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")


def remove_from_blacklist(request):
    id_ = request.POST['id']
    type_ = request.POST['type']
    if int(type_) == 1:
        BlackList.objects.filter(id=id_).delete()
    else:
        SuperBlacklist.objects.filter(id=id_).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")
