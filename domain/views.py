from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import models
from urllib import unquote
from domain.models import *
from domain.apps import *
from domain.lib import removeStuff
from basic_editing import main_filter
from whois_domain import main, main_period
from django.core.mail import send_mail
from django.conf import settings
from django.db import connection
from datetime import datetime, timedelta
from math import ceil
from os import popen
from operator import attrgetter
import requests, hashlib, traceback, json, csv
from random import randint
import re
from django.core import mail
from smtplib import SMTPServerDisconnected
import os
import binascii

hosts = [
    'webdomainexpert.us',
    'webdomainexpert.host',
    'webdomainexpert.site',
    'webdomainexpert.club',
]

@ensure_csrf_cookie
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect("/classified/")
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

# MANUAL
def manual(request):
    if request.user:
        logout(request)
    return render(request, 'manual.html', {})

def add_manual(request):
    file = request.POST['file'].replace('C:\\fakepath\\', '')
    with open(file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if len(row) > 1:
                name_zone = row[0].strip('"').replace(" ", "")
                email = row[1].strip('"').replace(" ", "")
                if email and '@' in email:
                    if not Emails.objects.filter(name_zone=name_zone, email=email).exists():
                        new = Emails(name_zone=name_zone, email=email)
                        new.save()

                    leads = RawLeads.objects.filter(name_zone=name_zone)
                    for lead in leads:
                        domain = email.split('@', 1)[1]
                        super_same_shit = ProcessTracker.objects.filter(email__endswith='@' + str(domain), name_redemption=lead.name_redemption)
                        super_same_shit_2 = RawLeads.objects.filter(mail__endswith='@' + str(domain), name_redemption=lead.name_redemption)

                        if super_same_shit.exists() or super_same_shit_2.exists():
                            datas = RawLeads.objects.filter(id=lead.id)
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

                    RawLeads.objects.filter(name_zone=name_zone).update(mail=email)

    removeStuff()

    return HttpResponse('{"status": "success"}', content_type="application/json")

# EDITING
def editing(request):
    if request.user:
        logout(request)
    sett = Setting.objects.get(id=1)
    return render(request, 'editing.html', {'sett': sett})

def changeSetting(request):
    name = request.POST['id']
    value = request.POST['value']
    Setting.objects.filter(id=1).update(**{ name: value })
    return HttpResponse('{"status": "success"}', content_type="application/json")

def runEditing(request):
    try:
        path = settings.BASE_DIR
        arg = request.POST['arg']
        if int(arg) == 1:
            script = '_basic_editing'
            language = 'pypy '
        else:
            script = 'basic_editing'
            language = 'pypy '
        com = request.POST['com'].replace('C:\\fakepath\\', '')
        net = request.POST['net'].replace('C:\\fakepath\\', '')
        org = request.POST['org'].replace('C:\\fakepath\\', '')
        info = request.POST['info'].replace('C:\\fakepath\\', '')
        us = request.POST['us'].replace('C:\\fakepath\\', '')

        e1 = request.POST['extra1'].replace('C:\\fakepath\\', '')
        e2 = request.POST['extra2'].replace('C:\\fakepath\\', '')
        e3 = request.POST['extra3'].replace('C:\\fakepath\\', '')
        e4 = request.POST['extra4'].replace('C:\\fakepath\\', '')

        redempt = request.POST['redempt'].replace('C:\\fakepath\\', '')
        date = request.POST['date']
        date = datetime.strptime(date, '%d-%m-%Y').date()

        to_del = RawLeads.objects.filter(date=date)
        hash_base_ids = map(attrgetter('hash_base_id'), to_del)
        RawLeads.objects.filter(date=date).delete()
        AllHash.objects.filter(hash_base_id__in=hash_base_ids).delete()


        argument = language + path + "/" + script + ".py "

        if com:
            argument += (com + " ")
        else:
            argument += "none "
        if net:
            argument += (net + " ")
        else:
            argument += "none "
        if org:
            argument += (org + " ")
        else:
            argument += "none "
        if info:
            argument += (info + " ")
        else:
            argument += "none "


        if us:
            argument += (us + " ")
        else:
            argument += "none "
        if e1:
            argument += (e1 + " ")
        else:
            argument += "none "
        if e2:
            argument += (e2 + " ")
        else:
            argument += "none "
        if e3:
            argument += (e3 + " ")
        else:
            argument += "none "
        if e4:
            argument += (e4 + " ")
        else:
            argument += "none "

        argument += (redempt + " " + str(date))
        popen(argument)
        # main_filter(com, net, org, info, redempt, date)
        return HttpResponse('{"status": "success"}', content_type="application/json")
    except:
        print traceback.format_exc(), argument
        return HttpResponse('{"status": "failed"}', content_type="application/json")


# RAW LEADS
def rawLeads(request):
    if request.user:
        logout(request)
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
    try:
        numbers += map(attrgetter('page'), RawLeads.objects.filter(date=date))
    except:
        pass
    number_of_pages = max(set(numbers))
    return render(
        request,
        'raw_leads.html',
        {
            "raw_leads": raw_leads,
            'range': range(1, number_of_pages + 1),
            'total_r': len(RawLeads.objects.filter(date=date, activated=0)),
            'total_a': len(RawLeads.objects.filter(date=date, activated=1)),
            'page': page,
        })


def reverse_state(request):
    if 'ids' in request.POST:
        ids = request.POST.get('ids')
        jd = json.dumps(ids)
        ids = eval(json.loads(jd))
        if 'true' in request.POST.get('foo'):
            mark = 1
        else:
            mark = 0
        RawLeads.objects.filter(id__in=ids).update(mark=mark)
        action = 'Marked ' if mark == 1 else 'Unmarked '

        ip = get_client_ip(request)
        el = EventLogger(ip=ip, action=(action + str(ids) + ""))
        el.save()

    else:
        raw_leads_id = int(unquote(request.POST['id']))
        mark = RawLeads.objects.get(id=raw_leads_id).mark
        mark += 1
        mark %= 2
        RawLeads.objects.filter(id=raw_leads_id).update(mark=mark)
        action = 'Marked ' if mark == 1 else 'Unmarked '

        ip = get_client_ip(request)
        el = EventLogger(ip=ip, action=(action + str(raw_leads_id) + ""))
        el = EventLogger(ip=ip, action=(action + str(raw_leads_id) + ""))
        el.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")


def select_all(request):
    page = request.POST['page']
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(page=page, date=date)
    raw_leads.update(mark=1)
    return HttpResponse('{"status": "success"}', content_type="application/json")


def add_this_name(request):
    ids = request.POST.get('ids')
    jd = json.dumps(ids)
    ids = eval(json.loads(jd))
    redemption = request.POST.get('redemption')
    page = request.POST.get('page')
    date = request.POST.get('date')
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(name_redemption=redemption, page=page, date=date, id__in=ids)
    raw_leads.update(mark=1)


    ip = get_client_ip(request)
    el = EventLogger(ip=ip, action="Marked " + str(ids) + " as good(1) ")
    el.save()

    return HttpResponse('{"status": "success"}', content_type="application/json")


def rem_this_name(request):
    ids = request.POST.get('ids')
    jd = json.dumps(ids)
    ids = eval(json.loads(jd))
    redemption = request.POST.get('redemption')
    page = request.POST.get('page')
    date = request.POST.get('date')
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(name_redemption=redemption, page=page, date=date, id__in=ids)
    raw_leads.update(mark=0)

    ip = get_client_ip(request)
    el = EventLogger(ip=ip, action="Unmarked " + str(ids) + "")
    el.save()

    return HttpResponse('{"status": "success"}', content_type="application/json")


def find_mails(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()

    if 'submit' in request.POST.keys():
        RawLeads.objects.filter(date=date, mark=1, activated=0).update(activated=1)

    main(date)
    return HttpResponse('{"status": "success"}', content_type="application/json")


def truncate(request):
    date = request.POST['date']
    activated = request.POST['activated']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(activated=activated, date=date)
    hash_base_ids = map(attrgetter('hash_base_id'), raw_leads)
    datas = RawLeads.objects.filter(activated=activated, date=date)
    for data in datas:
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='truncate'
        )
        record.save()
        RawLeads.objects.filter(id=data.id).delete()
    AllHash.objects.filter(hash_base_id__in=hash_base_ids).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")


# ACTIVE LEADS
def activeLeads(request):
    if 'date' in request.GET.keys():
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()


    raw_leads = RawLeads.objects.filter(activated=1, date=date, reminder=0)
    return render(
        request,
        'active_leads.html',
        {
            "raw_leads": raw_leads,
            'range': range(1, int(ceil(len(raw_leads) / 5000)) + 2),
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
    blacklists = RawLeads.objects.filter(blacklist=1, activated=1)
    for blacklist in blacklists:
        entry = BlackList.objects.filter(email=blacklist.mail)
        if not entry.exists():
            new = BlackList(email=blacklist.mail)
            new.save()
    raw_leads = RawLeads.objects.filter(blacklist=1, activated=1)
    hash_base_ids = map(attrgetter('hash_base_id'), raw_leads)

    datas = RawLeads.objects.filter(blacklist=1, activated=1)
    for data in datas:
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--blacklist_selected--'
        )
        record.save()

    RawLeads.objects.filter(blacklist=1, activated=1).delete()
    AllHash.objects.filter(hash_base_id__in=hash_base_ids).delete()

    return HttpResponse('{"status": "success"}', content_type="application/json")


def delete(request):
    if 'ids' in request.POST:
        ids = request.POST.get('ids')
        jd = json.dumps(ids)
        ids = eval(json.loads(jd))
        if 'true' in request.POST.get('foo'):
            to_delete = 1
        else:
            to_delete = 0
        RawLeads.objects.filter(id__in=ids, activated=1).update(to_delete=to_delete)
    else:
        leads_id = int(unquote(request.POST['id']))
        to_delete = RawLeads.objects.get(id=leads_id).to_delete
        to_delete += 1
        to_delete %= 2
        RawLeads.objects.filter(id=leads_id, activated=1).update(to_delete=to_delete)
    return HttpResponse('{"status": "success"}', content_type="application/json")


def mark_to_send(request):
    if 'ids' in request.POST:
        ids = request.POST.get('ids')
        jd = json.dumps(ids)
        ids = eval(json.loads(jd))
        if 'true' in request.POST.get('foo'):
            mark_to_send = 1
        else:
            mark_to_send = 0
        RawLeads.objects.filter(id__in=ids, activated=1).update(mark_to_send=mark_to_send)
    else:
        if 'id' in request.POST.keys():
            leads_id = int(unquote(request.POST['id']))
            mark_to_send = RawLeads.objects.get(id=leads_id).mark_to_send
            mark_to_send += 1
            mark_to_send %= 2
            RawLeads.objects.filter(id=leads_id, activated=1).update(mark_to_send=mark_to_send)
        else:
            date = request.POST['date']
            date = datetime.strptime(date, '%d-%m-%Y').date()
            RawLeads.objects.filter(date=date, activated=1).update(mark_to_send=1)
    return HttpResponse('{"status": "success"}', content_type="application/json")


def un_mark_to_send(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    RawLeads.objects.filter(date=date, activated=1).update(mark_to_send=0)
    return HttpResponse('{"status": "success"}', content_type="application/json")


def add_mail_man(request):
    mail = request.POST['email']
    lead_id = request.POST['id']
    name_zone = RawLeads.objects.get(id=lead_id).name_zone

    RawLeads.objects.filter(name_zone=name_zone).update(mail=mail)
    if Emails.objects.filter(name_zone=name_zone).exists():
        Emails.objects.filter(name_zone=name_zone).update(email=mail)
    else:
        new = Emails(name_zone=name_zone, email=mail)
        new.save()

    ids = map(attrgetter('id'), RawLeads.objects.filter(name_zone=name_zone))
    response = {
        'ids': ids,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


def rem_mail(request):
    lead_id = request.POST['id']
    name_zone = RawLeads.objects.get(id=lead_id).name_zone

    RawLeads.objects.filter(name_zone=name_zone).update(mail=None)
    Emails.objects.filter(name_zone=name_zone).delete()

    ids = map(attrgetter('id'), RawLeads.objects.filter(name_zone=name_zone))
    response = {
        'ids': ids,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


def send_mails(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()

    _to_delete = RawLeads.objects.filter(to_delete=1)
    delete_ids = map(attrgetter('hash_base_id'), _to_delete)
    # logging
    datas = RawLeads.objects.filter(to_delete=1, activated=1)
    for data in datas:
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--send_mails 1--'
        )
        record.save()
    # end logging
    delete = RawLeads.objects.filter(to_delete=1, activated=1).delete()

    blacklists = RawLeads.objects.filter(blacklist=1, activated=1)
    eml = []
    for blacklist in blacklists:
        entry = BlackList.objects.filter(email=blacklist.mail)
        eml.append(blacklist.mail)
        if not entry.exists():
            new = BlackList(email=blacklist.mail)
            new.save()
    _to_blacklist = RawLeads.objects.filter(mail__in=eml)
    blacklist_ids = map(attrgetter('hash_base_id'), _to_delete)

    # logging
    datas = RawLeads.objects.filter(mail__in=eml)
    for data in datas:
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--send_mails 2--'
        )
        record.save()
    # end logging
    delete = RawLeads.objects.filter(mail__in=eml).delete()

    AllHash.objects.filter(hash_base_id__in=blacklist_ids + delete_ids)

    potential_profits = RawLeads.objects.filter(date=date, mark_to_send=1, mail__isnull=False, reminder=0)

    connection = mail.get_connection()
    connection.open()
    asdi = 0
    for potential_profit in potential_profits:
        hash_base_id = potential_profit.hash_base_id
        try:
            iterator = randint(0, 3)
            link = ('http://www.' + str(hosts[iterator]) + '/offer/?id=' + str(hash_base_id))
            unsubscribe = ('http://www.' + str(hosts[iterator]) + '/unsubscribe/?id=' + str(hash_base_id))
            # case = randint(1, 10)
            case = 1
            msg = eval('form_a_msg' + str(case) + '("' + str(potential_profit.name_redemption) + '","' + str(
                link) + '","' + str(unsubscribe) + '")')

            req = requests.post(
                "http://www.webdomainexpert.pw/add_offer/",
                data={
                    'base_id': potential_profit.id,
                    'drop': potential_profit.name_redemption,
                    'lead': potential_profit.name_zone,
                    'hash_base_id': hash_base_id,
                    'remail': potential_profit.mail,
                }
            )
            if req.status_code == 204:
                hash = hashlib.md5()
                hash.update(str(potential_profit.id + 100000))
                hash_base_id = hash.hexdigest()

                req = requests.post(
                    "http://www.webdomainexpert.pw/add_offer/",
                    data={
                        'base_id': potential_profit.id,
                        'drop': potential_profit.name_redemption,
                        'lead': potential_profit.name_zone,
                        'hash_base_id': hash_base_id,
                        'remail': potential_profit.mail,
                    }
                )

            if req.status_code == 200:
                AllHash.objects.filter(hash_base_id=hash_base_id)
                # RawLeads.objects.filter(id=potential_profit.id).delete()
                RawLeads.objects.filter(id=potential_profit.id).update(reminder=1, hash_base_id=hash_base_id)

                emails = []
                email = mail.EmailMultiAlternatives(
                    msg[0],
                    'potential_profit.name_zone',
                    'Web Domain Expert <' + str(settings.EMAIL_HOST_USER) + '>',
                    [potential_profit.mail],
                    reply_to=("support@webdomainexpert.com", ),
                    bcc=["bcc-webdomainexpert@outlook.com"],
                )
                email.attach_alternative(msg[1], "text/html")
                emails.append(email)
                try:
                    connection.send_messages(emails)
                    asdi += 1
                except SMTPServerDisconnected:
                    connection = mail.get_connection()
                    connection.open()
                    connection.send_messages(emails)
        except:
            print traceback.format_exc()
    connection.close()

    if not Log.objects.filter(date=datetime.now().date()).exists():
        Log().save()
    number_of_old = Log.objects.get(date=datetime.now().date()).number_sent
    number_of_old_2 = Log.objects.get(date=date).number_sent_2
    Log.objects.filter(date=datetime.now().date()).update(number_sent=(int(asdi) + int(number_of_old)))
    Log.objects.filter(date=date).update(number_sent_2=(int(asdi) + int(number_of_old_2)))

    return HttpResponse('{"status": "success"}', content_type="application/json")


def blacklisting(request):
    if request.user:
        logout(request)
    blacklist = BlackList.objects.all()
    superblacklist = SuperBlacklist.objects.all()
    return render(request, 'super_blacklist.html', {
        'blacklist': blacklist,
        'superblacklist': superblacklist,
    })


def super_blacklist(request):
    domain = request.POST['domain']
    domain = "".join(domain.split())
    entry = SuperBlacklist.objects.filter(domain=domain)
    if not entry.exists():
        new_entry = SuperBlacklist(domain=domain)
        new_entry.save()
    exclude_email = '@' + str(domain)

    super_b_l = RawLeads.objects.filter(mail__endswith=exclude_email)
    hash_base_ids = map(attrgetter('hash_base_id'), super_b_l)

    # logging
    datas = RawLeads.objects.filter(hash_base_id__in=hash_base_ids)
    for data in datas:
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--super_blacklist--'
        )
        record.save()
    # end logging

    RawLeads.objects.filter(hash_base_id__in=hash_base_ids).delete()
    AllHash.objects.filter(hash_base_id__in=hash_base_ids).delete()

    return HttpResponse('{"status": "success"}', content_type="application/json")


def regular_blacklist(request):
    email = request.POST['email']
    email = "".join(email.split())
    entry = BlackList.objects.filter(email=email)
    if not entry.exists():
        new_entry = BlackList(email=email)
        new_entry.save()

    b_l = RawLeads.objects.filter(mail=email)
    hash_base_ids = map(attrgetter('hash_base_id'), b_l)

    # logging
    datas = RawLeads.objects.filter(hash_base_id__in=hash_base_ids)
    for data in datas:
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--regular_blacklist--'
        )
        record.save()
    # end logging

    RawLeads.objects.filter(hash_base_id__in=hash_base_ids).delete()
    AllHash.objects.filter(hash_base_id__in=hash_base_ids).delete()

    return HttpResponse('{"status": "success"}', content_type="application/json")


def remove_from_blacklist(request):
    id_ = request.POST['id']
    type_ = request.POST['type']
    if int(type_) == 1:
        BlackList.objects.filter(id=id_).delete()
    else:
        SuperBlacklist.objects.filter(id=id_).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")

def download(request):
    file = open('zone_with_no_emails.txt', 'w')
    file.seek(0)
    file.truncate()

    all_ = []
    datas = RawLeads.objects.filter(activated=1, mail__isnull=True)
    for data in datas:
        if data.name_zone not in all_:
            file.write(data.name_zone + '\n')
            all_.append(data.name_zone)
    file.close()

    f = open('zone_with_no_emails.txt', "rb")
    res = HttpResponse(f)
    res['Content-Disposition'] = 'attachment; filename=zone_with_no_email.txt'
    return res

def add_multiple(request):
    items = request.POST.get('dict')
    jd = json.dumps(items)
    items = eval(json.loads(jd))
    for item in items:
        RawLeads.objects.filter(id=item['id']).update(mail=item['value'])
    return HttpResponse('{"status": "success"}', content_type="application/json")

def active_manual(request):
    _id = request.POST['id']
    potential_profit = RawLeads.objects.get(id=_id)
    req = requests.post(
        "http://www.webdomainexpert.pw/add_offer/",
        data={
            'base_id': potential_profit.id,
            'drop': potential_profit.name_redemption,
            'lead': potential_profit.name_zone,
            'hash_base_id': potential_profit.hash_base_id,
            'remail': potential_profit.mail,
        }
    )
    if req.status_code == 200:
        return HttpResponse('{"status": "success"}', content_type="application/json")
    else:
        return HttpResponse(status=req.status_code)

@csrf_exempt
def del_hash(request):
    hash_base_id = request.POST['hash_base_id']
    AllHash.objects.filter(hash_base_id=hash_base_id).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")

def find_active(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(activated=0, date=date)
    for raw_lead in raw_leads:
        drop = raw_lead.name_redemption.split('.')[0]
        zone = raw_lead.name_zone.split('.')[0]
        if drop == zone:
            RawLeads.objects.filter(id=raw_lead.id).update(activated=1)
    return HttpResponse('{"status": "success"}', content_type="application/json")


# SEARCH
def search(request):
    if request.user:
        logout(request)
    return render(request, 'search.html', {})

def search_results(request):
    if request.user:
        logout(request)
    name_redemption = request.POST['drop_domain']
    name_zone = request.POST['zone_domain']
    datepicker = request.POST['datepicker']
    try:
        date = datetime.strptime(datepicker, '%d-%m-%Y').date()
        search_leads = RawLeads.objects.filter(
            name_zone__contains=name_zone,
            name_redemption__contains=name_redemption,
            date=date,
        )[0:150]
        search_dels = DeletedInfo.objects.filter(
            name_zone__contains=name_zone,
            name_redemption__contains=name_redemption,
            date=date,
        )[0:50]
    except:
        search_leads = RawLeads.objects.filter(
            name_zone__contains=name_zone,
            name_redemption__contains=name_redemption
        )[0:200]
        search_dels = DeletedInfo.objects.filter(
            name_zone__contains=name_zone,
            name_redemption__contains=name_redemption
        )[0:50]
    return render(request, 'search.html', {'search_leads': search_leads, 'search_dels': search_dels})

def send_pending(request):
    potential_profits = RawLeads.objects.filter(activated=1, mail__isnull=False, reminder=0)

    connection = mail.get_connection()
    connection.open()
    asdi = 0
    for potential_profit in potential_profits:
        hash_base_id = potential_profit.hash_base_id
        try:
            iterator = randint(0, 3)
            link = ('http://www.' + str(hosts[iterator]) + '/offer/?id=' + str(hash_base_id))
            unsubscribe = ('http://www.' + str(hosts[iterator]) + '/unsubscribe/?id=' + str(hash_base_id))
            # case = randint(1, 10)
            case = 1
            msg = eval('form_a_msg' + str(case) + '("' + str(potential_profit.name_redemption) + '","' + str(
                link) + '","' + str(unsubscribe) + '")')

            req = requests.post(
                "http://www.webdomainexpert.pw/add_offer/",
                data={
                    'base_id': potential_profit.id,
                    'drop': potential_profit.name_redemption,
                    'lead': potential_profit.name_zone,
                    'hash_base_id': hash_base_id,
                    'remail': potential_profit.mail,
                }
            )
            if req.status_code == 204:
                hash = hashlib.md5()
                hash.update(str(potential_profit.id + 100000))
                hash_base_id = hash.hexdigest()

                req = requests.post(
                    "http://www.webdomainexpert.pw/add_offer/",
                    data={
                        'base_id': potential_profit.id,
                        'drop': potential_profit.name_redemption,
                        'lead': potential_profit.name_zone,
                        'hash_base_id': hash_base_id,
                        'remail': potential_profit.mail,
                    }
                )

            if req.status_code == 200:
                AllHash.objects.filter(hash_base_id=hash_base_id)
                # RawLeads.objects.filter(id=potential_profit.id).delete()
                RawLeads.objects.filter(id=potential_profit.id).update(reminder=1, hash_base_id=hash_base_id)

                emails = []
                email = mail.EmailMultiAlternatives(
                    msg[0],
                    'potential_profit.name_zone',
                    'Web Domain Expert <' + str(settings.EMAIL_HOST_USER) + '>',
                    [potential_profit.mail],
                    reply_to=("support@webdomainexpert.com", ),
                    bcc=["bcc-webdomainexpert@outlook.com"],
                )
                email.attach_alternative(msg[1], "text/html")
                emails.append(email)
                try:
                    connection.send_messages(emails)
                    asdi += 1

                    number_of_old_2 = Log.objects.get(date=potential_profit.date).number_sent_2
                    Log.objects.filter(date=potential_profit.date).update(number_sent_2=(1 + int(number_of_old_2)))

                except SMTPServerDisconnected:
                    connection = mail.get_connection()
                    connection.open()
                    connection.send_messages(emails)
        except:
            print traceback.format_exc()
    connection.close()

    if not Log.objects.filter(date=datetime.now().date()).exists():
        Log().save()
    number_of_old = Log.objects.get(date=datetime.now().date()).number_sent
    Log.objects.filter(date=datetime.now().date()).update(number_sent=(int(asdi) + int(number_of_old)))

    return HttpResponse('{"status": "success"}', content_type="application/json")

def whois_period(request):
    interval = int(request.POST['interval'])
    dates = []
    for i in range(0, interval):
        date = (datetime.now() - timedelta(days=i)).date()
        dates.append(date)
    main_period(dates)
    return HttpResponse('{"status": "success"}', content_type="application/json")

@login_required
def admin(request):
    if 'date' in request.GET.keys():
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now().date()

    try:
        log = Log.objects.get(date=date)
    except Log.DoesNotExist:
        log = None

    if log:
        data_to_show = {
            'number_act':log.number_act if log else 0,
            'number_sent':log.number_sent if log else 0,
            'number_act_2':log.number_act_2 if log else 0,
            'number_sent_2':log.number_sent_2 if log else 0,
            'number_of_redemption': log.number_of_redemption,
            'number_of_all': log.number_of_all,
            'duration': log.duration,
        }
    else:
        data_to_show = None

    return render(
        request,
        'classified.html',
        {
            "log": data_to_show,
            'total_r': len(RawLeads.objects.filter(date=date, activated=0)),
            'total_a': len(RawLeads.objects.filter(date=date, activated=1)),
            'exceptions': DomainException.objects.all()
        })

@login_required
def removeUnwanted(request):
    removeStuff()
    return HttpResponse('{"status": "success"}', content_type="application/json")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def deleteException(request):
    id_ = request.POST['id']
    DomainException.objects.filter(id=id_).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")

def addException(request):
    domain = request.POST['name']
    DomainException(domain=domain).save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

def restoreDeleted(request):
    id_ = request.POST['id']
    deleted = DeletedInfo.objects.get(id=id_)
    condition = True
    while condition:
        try:
            entry = RawLeads(
                name_zone=deleted.name_zone,
                name_redemption=deleted.name_redemption,
                date=deleted.date,
                mail=deleted.email,
                page=1,
                activated=1,
                hash_base_id=binascii.hexlify(os.urandom(16))
            )
            entry.save()
            condition = False
        except:
            pass
    DeletedInfo.objects.filter(id=id_).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")



