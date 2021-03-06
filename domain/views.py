from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.db import models
from urllib import unquote
from domain.models import *
from domain.apps import *
from domain.lib import removeStuff
from whois_domain import main, main_period, main_submit
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
from django.utils import timezone
from el_pagination.decorators import page_template

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
            if user.has_perm('domain.user'):
                return HttpResponseRedirect("/raw_leads/")
            else:
                return HttpResponseRedirect("/")
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return HttpResponseRedirect("/home_login/")

# MANUAL
@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.user", "domain.admin"]))
def manual(request):
    return render(request, 'manual.html', {})

@csrf_exempt
def add_manual(request):
    file = request.POST['file'].replace('C:\\fakepath\\', '')
    with open(file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if len(row) > 1:
                name_zone = row[0].strip('"').replace(" ", "")
                email = row[1].strip('"').replace(" ", "")

                email = email.replace('RegistrantEmail:', '')
                if email and '@' in email:
                    if not Emails.objects.filter(name_zone=name_zone, email=email).exists():
                        new = Emails(name_zone=name_zone, email=email)
                        new.save()

                    leads = RawLeads.objects.filter(name_zone=name_zone)
                    for lead in leads:
                        domain = email.split('@', 1)[1]
                        c_domain = domain.split('.', 1)[0]
                        super_same_shit = ProcessTracker.objects.filter(email__endswith='@' + str(domain), name_redemption=lead.name_redemption)
                        super_same_shit_2 = RawLeads.objects.filter(mail__endswith='@' + str(domain), name_redemption=lead.name_redemption)

                        if (super_same_shit.exists() or super_same_shit_2.exists()) and not (DomainException.objects.filter(domain=c_domain).exists() or DomainException.objects.filter(domain=domain).exists):
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

                        # RawLeads.objects.filter(name_zone=name_zone).update(mail=email)
                    rls = RawLeads.objects.filter(name_zone=name_zone)
                    for rl in rls:
                        rl.mail = email
                        rl.save()

    removeStuff()

    return HttpResponse('{"status": "success"}', content_type="application/json")

# EDITING.
@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.user", "domain.admin"]))
def editing(request):
    sett = Setting.objects.get(id=1)
    zone_data = {
        'com': ZoneFiles.objects.get(zone_type='com').zone_name,
        'net': ZoneFiles.objects.get(zone_type='net').zone_name,
        'org': ZoneFiles.objects.get(zone_type='org').zone_name,
        'info': ZoneFiles.objects.get(zone_type='info').zone_name,
        'us': ZoneFiles.objects.get(zone_type='us').zone_name,
        'biz': ZoneFiles.objects.get(zone_type='biz').zone_name,
        'mobi': ZoneFiles.objects.get(zone_type='mobi').zone_name,
    }
    return render(request, 'editing.html', {'sett': sett, 'zone_data': zone_data})

@csrf_exempt
def changeSetting(request):
    name = request.POST['id']
    value = request.POST['value']
    Setting.objects.filter(id=1).update(**{ name: value })
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def runEditing(request):
    try:
        path = settings.BASE_DIR
        arg = request.POST['arg']
        if int(arg) == 1:
            script = 'testing'
            language = 'python '
        else:
            script = 'testing'
            language = 'pypy '

        redempt = request.POST['redempt'].replace('C:\\fakepath\\', '')
        redempt2 = request.POST['redempt2'].replace('C:\\fakepath\\', '')
        redempt3 = request.POST['redempt3'].replace('C:\\fakepath\\', '')

        answer = request.POST['answer'].replace('C:\\fakepath\\', '')

        date = request.POST['date']
        date = datetime.strptime(date, '%d-%m-%Y').date()

        if answer == 'yes':
            to_del = RawLeads.objects.filter(date=date)
            hash_base_ids = map(attrgetter('hash_base_id'), to_del)
            RawLeads.objects.filter(date=date).delete()
            AllHash.objects.filter(hash_base_id__in=hash_base_ids).delete()

        argument = language + path + "/" + script + ".py "
        argument += (redempt + " ")

        if redempt2:
            argument += (redempt2 + " ")
        else:
            argument += "none "

        argument += str(date)
        print argument
        popen(argument)
        return HttpResponse('{"status": "success"}', content_type="application/json")
    except:
        print traceback.format_exc(), argument
        return HttpResponse('{"status": "failed"}', content_type="application/json")

#RAW LEADS
@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.user", "domain.admin"]))
@page_template('raw_leads_index.html')
def rawLeads(request, template='raw_leads.html', extra_context=None):
    if 'date' in request.GET.keys() and len(request.GET['date']) > 6:
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()
    if 'pages' in request.GET.keys():
        page = int(request.GET['pages'])
    else:
        page = 1
    if 'list_no' in request.GET.keys():
        list_no = int(request.GET['list_no'])
    else:
        list_no = 1

    raw_leads = RawLeads.objects.filter(date=date, activated=0, page=page, list_no=list_no).order_by('name_redemption')
    numbers = [1]
    try:
        numbers += map(attrgetter('page'), RawLeads.objects.filter(date=date, list_no=list_no))
    except:
        pass
    number_of_pages = max(set(numbers))

    context = {
        "raw_leads": raw_leads,
        'range': range(1, number_of_pages + 1),
        'page': page,
        'list_no': list_no,
        'offset': (int(request.GET['page']) - 1) * 1000 if 'page' in request.GET.keys() else 0,
        'date': datetime.strftime(date, '%d-%m-%Y'),
        'page_template': page_template,
        'total_raw': len(RawLeads.objects.filter(date=date, page=page, activated=0, list_no=list_no)),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.user", "domain.admin"]))
def rawLeadsAll(request):
    if 'date' in request.GET.keys() and len(request.GET['date']) > 6:
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()
    if 'pages' in request.GET.keys():
        page = int(request.GET['pages'])
    else:
        page = 1
    if 'list_no' in request.GET.keys():
        list_no = int(request.GET['list_no'])
    else:
        list_no = 1

    raw_leads = RawLeads.objects.filter(date=date, activated=0, page=page, list_no=list_no)
    numbers = [1]
    try:
        numbers += map(attrgetter('page'), RawLeads.objects.filter(date=date, list_no=list_no))
    except:
        pass
    number_of_pages = max(set(numbers))
    return render(
        request,
        'raw_leads_all.html',
        {
            "raw_leads": raw_leads,
            'range': range(1, number_of_pages + 1),
            'page': page,
            'list_no': list_no,
            'total_raw': len(RawLeads.objects.filter(date=date, page=page, activated=0, list_no=list_no)),
        })

@csrf_exempt
def reverse_state(request):
    if 'ids' in request.POST:
        ids = request.POST.get('ids')
        jd = json.dumps(ids)
        ids = eval(json.loads(jd))
        if 'true' in request.POST.get('foo'):
            mark = 1
        else:
            mark = 0
        rls = RawLeads.objects.filter(id__in=ids)
        for rl in rls:
            rl.mark = mark
            rl.save()
        action = 'Marked ' if mark == 1 else 'Unmarked '

        ip = get_client_ip(request)
        msg = str(ids)[0:9950]
        if len(str(ids)) > 10000:
            msg += '...'
        el = EventLogger(ip=ip, action=(action + msg + ""))
        el.save()

    else:
        raw_leads_id = int(unquote(request.POST['id']))
        mark = RawLeads.objects.get(id=raw_leads_id).mark
        mark += 1
        mark %= 2
        # RawLeads.objects.filter(id=raw_leads_id).update(mark=mark)

        rls = RawLeads.objects.filter(id=raw_leads_id)
        for rl in rls:
            rl.mark = mark
            rl.save()

        action = 'Marked ' if mark == 1 else 'Unmarked '

        ip = get_client_ip(request)
        msg = str(raw_leads_id)[0:9950]
        if len(str(raw_leads_id)) > 10000:
            msg += '...'
        el = EventLogger(ip=ip, action=(action + msg + ""))
        el.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def add_this_name(request):
    ids = request.POST.get('ids')
    jd = json.dumps(ids)
    ids = eval(json.loads(jd))
    redemption = request.POST.get('redemption')
    page = request.POST.get('page')
    date = request.POST.get('date')
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(name_redemption=redemption, page=page, date=date, id__in=ids)
    # raw_leads.update(mark=1)
    for rl in raw_leads:
        rl.mark = 1
        rl.save()

    ip = get_client_ip(request)
    msg = str(ids)[0:9950]
    if len(str(ids)) > 10000:
        msg += '...'

    el = EventLogger(ip=ip, action="Marked " + msg + " as good(1) ")
    el.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def rem_this_name(request):
    ids = request.POST.get('ids')
    jd = json.dumps(ids)
    ids = eval(json.loads(jd))
    redemption = request.POST.get('redemption')
    page = request.POST.get('page')
    date = request.POST.get('date')
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(name_redemption=redemption, page=page, date=date, id__in=ids)
    # raw_leads.update(mark=0)
    for rl in raw_leads:
        rl.mark = 0
        rl.save()

    ip = get_client_ip(request)
    msg = str(ids)[0:9950]
    if len(str(ids)) > 10000:
        msg += '...'

    el = EventLogger(ip=ip, action="Unmarked " + msg + "")
    el.save()

    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def find_mails(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()

    if 'submit' in request.POST.keys():
        if not Log.objects.filter(date=datetime.now().date()).exists():
            Log().save()
        number_of_new = len(RawLeads.objects.filter(date=date, mark=1, activated=0))

        number_of_old = Log.objects.get(date=datetime.now().date()).number_act
        # Log.objects.filter(date=datetime.now().date()).update(number_act=(int(number_of_old) + int(number_of_new)))
        ls = Log.objects.filter(date=datetime.now().date())
        for l in ls:
            l.number_act = (int(number_of_old) + int(number_of_new))
            l.save()

        if not Log.objects.filter(date=date).exists():
            Log(date=date).save()
        number_of_old_2 = Log.objects.get(date=date).number_act_2
        # Log.objects.filter(date=date).update(number_act_2=(int(number_of_old_2) + int(number_of_new)))
        ls = Log.objects.filter(date=date)
        for l in ls:
            l.number_act_2 = (int(number_of_old_2) + int(number_of_new))
            l.save()

        # RawLeads.objects.filter(date=date, mark=1, activated=0).update(activated=1, mark=0)
        rls = RawLeads.objects.filter(date=date, mark=1, activated=0)
        for rl in rls:
            rl.activated = 1
            rl.mark = 0
            rl.save()

        main_submit(date)
    else:
        mode = request.POST['mode']
        main(date, mode)
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def truncate(request):
    date = request.POST['date']
    activated = request.POST['activated']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    hash_base_ids = []
    datas = RawLeads.objects.filter(activated=activated, date=date)
    for data in datas:
        hash_base_ids.append(data.hash_base_id)
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
@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.user", "domain.admin"]))
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
            'total_a': len(raw_leads),
        })

@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.user", "domain.admin"]))
def activeLeadsTld(request):
    if 'date' in request.GET.keys():
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()

    raw_leads = RawLeads.objects.filter(activated=2, date=date, reminder=0)
    return render(
        request,
        'active_leads_tld.html',
        {
            "raw_leads": raw_leads,
            'range': range(1, int(ceil(len(raw_leads) / 5000)) + 2),
            'total_a': len(raw_leads),
        })

@csrf_exempt
def blacklist(request):
    leads_id = int(unquote(request.POST['id']))
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    blacklist = RawLeads.objects.get(id=leads_id).blacklist
    blacklist += 1
    blacklist %= 2
    mail = RawLeads.objects.get(id=leads_id).mail
    # RawLeads.objects.filter(mail=mail, activated=1).update(blacklist=blacklist)
    rls = RawLeads.objects.filter(mail=mail, activated__gte=1)
    for rl in rls:
        rl.blacklist = blacklist
        rl.save()

    ids = map(attrgetter('id'), RawLeads.objects.filter(mail=mail, activated__gte=1, date=date))
    response = {
        'ids': ids,
        'command': True if blacklist else False
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def blacklist_selected(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    blacklists = RawLeads.objects.filter(blacklist=1, activated__gte=1, date=date)
    for blacklist in blacklists:
        entry = BlackList.objects.filter(email=blacklist.mail)
        if not entry.exists():
            new = BlackList(email=blacklist.mail)
            new.save()

    hash_base_ids = []
    datas = RawLeads.objects.filter(blacklist=1, activated__gte=1, date=date)
    for data in datas:
        hash_base_ids.append(data.hash_base_id)
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--blacklist_selected--'
        )
        record.save()

    RawLeads.objects.filter(blacklist=1, activated__gte=1, date=date).delete()
    AllHash.objects.filter(hash_base_id__in=hash_base_ids).delete()

    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def delete(request):
    if 'ids' in request.POST:
        ids = request.POST.get('ids')
        jd = json.dumps(ids)
        ids = eval(json.loads(jd))
        if 'true' in request.POST.get('foo'):
            to_delete = 1
        else:
            to_delete = 0
        # RawLeads.objects.filter(id__in=ids, activated=1).update(to_delete=to_delete)
        rls = RawLeads.objects.filter(id__in=ids, activated__gte=1)
        for rl in rls:
            rl.to_delete = to_delete
            rl.save()
    else:
        leads_id = int(unquote(request.POST['id']))
        to_delete = RawLeads.objects.get(id=leads_id).to_delete
        to_delete += 1
        to_delete %= 2
        # RawLeads.objects.filter(id=leads_id, activated=1).update(to_delete=to_delete)
        rls = RawLeads.objects.filter(id=leads_id, activated__gte=1)
        for rl in rls:
            rl.to_delete = to_delete
            rl.save()

    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def mark_to_send(request):
    activated = request.POST.get('activated')
    if 'ids' in request.POST:
        ids = request.POST.get('ids')
        jd = json.dumps(ids)
        ids = eval(json.loads(jd))
        if 'true' in request.POST.get('foo'):
            mark_to_send = 1
        else:
            mark_to_send = 0
        # RawLeads.objects.filter(id__in=ids, activated=1).update(mark_to_send=mark_to_send)
        rls = RawLeads.objects.filter(id__in=ids,  activated=activated)
        for rl in rls:
            rl.mark_to_send = mark_to_send
            rl.save()
    else:
        if 'id' in request.POST.keys():
            leads_id = int(unquote(request.POST['id']))
            mark_to_send = RawLeads.objects.get(id=leads_id).mark_to_send
            mark_to_send += 1
            mark_to_send %= 2
            # RawLeads.objects.filter(id=leads_id, activated=1).update(mark_to_send=mark_to_send)
            rls = RawLeads.objects.filter(id=leads_id,  activated=activated)
            for rl in rls:
                rl.mark_to_send = mark_to_send
                rl.save()
        else:
            date = request.POST['date']
            date = datetime.strptime(date, '%d-%m-%Y').date()
            # RawLeads.objects.filter(date=date, activated=1).update(mark_to_send=1)
            rls = RawLeads.objects.filter(date=date, activated=activated)
            for rl in rls:
                rl.mark_to_send = 1
                rl.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def un_mark_to_send(request):
    date = request.POST['date']
    activated = request.POST['activated']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    # RawLeads.objects.filter(date=date, activated=1).update(mark_to_send=0)
    rls = RawLeads.objects.filter(date=date,  activated=activated)
    for rl in rls:
        rl.mark_to_send = 0
        rl.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def add_mail_man(request):
    mail = request.POST['email']
    lead_id = request.POST['id']
    name_zone = RawLeads.objects.get(id=lead_id).name_zone

    # RawLeads.objects.filter(name_zone=name_zone).update(mail=mail)
    rls = RawLeads.objects.filter(name_zone=name_zone)
    for rl in rls:
        mail = mail.replace('RegistrantEmail:', '')
        rl.mail = mail
        rl.save()

    if Emails.objects.filter(name_zone=name_zone).exists():
        # Emails.objects.filter(name_zone=name_zone).update(email=mail)
        ems = Emails.objects.filter(name_zone=name_zone)
        for em in ems:
            em.email = mail
            em.save()
    else:
        new = Emails(name_zone=name_zone, email=mail)
        new.save()

    ids = map(attrgetter('id'), RawLeads.objects.filter(name_zone=name_zone))
    response = {
        'ids': ids,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def rem_mail(request):
    lead_id = request.POST['id']
    name_zone = RawLeads.objects.get(id=lead_id).name_zone

    # RawLeads.objects.filter(name_zone=name_zone).update(mail=None)
    rls = RawLeads.objects.filter(name_zone=name_zone)
    for rl in rls:
        rl.mail = None
        rl.save()

    Emails.objects.filter(name_zone=name_zone).delete()

    ids = map(attrgetter('id'), RawLeads.objects.filter(name_zone=name_zone))
    response = {
        'ids': ids,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def send_mails(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()

    delete_ids = []
    # logging
    datas = RawLeads.objects.filter(to_delete=1, activated__gte=1)
    for data in datas:
        delete_ids.append(data.hash_base_id)
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--send_mails 1, to_delete=1--'
        )
        record.save()
    # end logging
    RawLeads.objects.filter(to_delete=1, activated__gte=1).delete()

    blacklists = RawLeads.objects.filter(blacklist=1, activated__gte=1)
    eml = []
    for blacklist in blacklists:
        entry = BlackList.objects.filter(email=blacklist.mail)
        eml.append(blacklist.mail)
        if not entry.exists():
            new = BlackList(email=blacklist.mail)
            new.save()

    # logging
    datas = RawLeads.objects.filter(mail__in=eml)
    for data in datas:
        delete_ids.append(data.hash_base_id)
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--send_mails 2, blacklist=1--'
        )
        record.save()
    # end logging
    delete = RawLeads.objects.filter(mail__in=eml).delete()

    AllHash.objects.filter(hash_base_id__in=delete_ids)

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
            while req.status_code == 204:
                hash_base_id = binascii.hexlify(os.urandom(16))

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
                    # AllHash.objects.filter(hash_base_id=potential_profit.hash_base_id).update(hash_base_id=hash_base_id)
                als = AllHash.objects.filter(hash_base_id=potential_profit.hash_base_id)
                for al in als:
                    al.hash_base_id = hash_base_id
                    al.save()

                    # RawLeads.objects.filter(id=potential_profit.id).update(reminder=1, hash_base_id=hash_base_id, last_email_date=timezone.now())
                rls = RawLeads.objects.filter(id=potential_profit.id)
                for rl in rls:
                    rl.reminder = 1
                    rl.hash_base_id = hash_base_id
                    rl.last_email_date = timezone.now()
                    rl.save()

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
                    asdi += 1
        except:
            return HttpResponse(traceback.format_exc(), content_type='application/json')
    connection.close()

    if not Log.objects.filter(date=datetime.now().date()).exists():
        Log().save()
    number_of_old = Log.objects.get(date=datetime.now().date()).number_sent
    if not Log.objects.filter(date=date).exists():
        Log(date=date).save()
    number_of_old_2 = Log.objects.get(date=date).number_sent_2

    # Log.objects.filter(date=datetime.now().date()).update(number_sent=(int(asdi) + int(number_of_old)))
    ls = Log.objects.filter(date=datetime.now().date())
    for l in ls:
        l.number_sent = (int(asdi) + int(number_of_old))
        l.save()

    # Log.objects.filter(date=date).update(number_sent_2=(int(asdi) + int(number_of_old_2)))
    ls = Log.objects.filter(date=date)
    for l in ls:
        l.number_sent_2 = (int(asdi) + int(number_of_old_2))
        l.save()

    return HttpResponse('{"status": "success"}', content_type="application/json")

@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.admin"]))
def blacklisting(request):
    blacklist = BlackList.objects.all()
    superblacklist = SuperBlacklist.objects.all()
    return render(request, 'super_blacklist.html', {
        'blacklist': blacklist,
        'superblacklist': superblacklist,
    })

@csrf_exempt
def super_blacklist(request):
    domain = request.POST['domain']
    domain = "".join(domain.split())
    entry = SuperBlacklist.objects.filter(domain=domain)
    if not entry.exists():
        new_entry = SuperBlacklist(domain=domain)
        new_entry.save()
    exclude_email = '@' + str(domain)

    hash_base_ids = []
    # logging
    datas = RawLeads.objects.filter(mail__endswith=exclude_email)
    for data in datas:
        hash_base_ids.append(data.hash_base_id)
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--super_blacklist--'
        )
        record.save()
    # end logging
    RawLeads.objects.filter(mail__endswith=exclude_email).delete()
    AllHash.objects.filter(hash_base_id__in=hash_base_ids).delete()

    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def regular_blacklist(request):
    email = request.POST['email']
    email = "".join(email.split())
    entry = BlackList.objects.filter(email=email)
    if not entry.exists():
        new_entry = BlackList(email=email)
        new_entry.save()

    hash_base_ids = []
    # logging
    datas = RawLeads.objects.filter(mail__iexact=email)
    for data in datas:
        hash_base_ids.append(data.hash_base_id)
        record = DeletedInfo(
            name_zone=data.name_zone,
            name_redemption=data.name_redemption,
            date=data.date,
            email=data.mail,
            reason='--regular_blacklist--'
        )
        record.save()
    # end logging

    RawLeads.objects.filter(mail__iexact=email).delete()
    AllHash.objects.filter(hash_base_id__in=hash_base_ids).delete()

    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def remove_from_blacklist(request):
    id_ = request.POST['id']
    type_ = request.POST['type']
    if int(type_) == 1:
        BlackList.objects.filter(id=id_).delete()
    else:
        SuperBlacklist.objects.filter(id=id_).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def download_all(request):
    file = open('zone_with_no_emails.txt', 'w')
    file.seek(0)
    file.truncate()

    all_ = []
    datas = RawLeads.objects.filter(activated__gte=1, mail__isnull=True).order_by('-id')
    for data in datas:
        if data.name_zone not in all_:
            file.write(data.name_zone + '\n')
            all_.append(data.name_zone)
    file.close()

    f = open('zone_with_no_emails.txt', "rb")
    res = HttpResponse(f)
    res['Content-Disposition'] = 'attachment; filename=zone_with_no_email.txt'
    return res

@csrf_exempt
def download(request):
    if 'date' in request.GET.keys():
        date = request.GET['date']
        date = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        date = datetime.now().date()

    file = open('zone_with_no_emails.txt', 'w')
    file.seek(0)
    file.truncate()

    all_ = []
    datas = RawLeads.objects.filter(activated__gte=1, mail__isnull=True, date=date).order_by('-id')
    for data in datas:
        if data.name_zone not in all_:
            file.write(data.name_zone + '\n')
            all_.append(data.name_zone)
    file.close()

    f = open('zone_with_no_emails.txt', "rb")
    res = HttpResponse(f)
    res['Content-Disposition'] = 'attachment; filename=zone_with_no_email.txt'
    return res

@csrf_exempt
def add_multiple(request):
    items = request.POST.get('dict')
    jd = json.dumps(items)
    items = eval(json.loads(jd))
    for item in items:
            # RawLeads.objects.filter(id=item['id']).update(mail=item['value'])
        rls = RawLeads.objects.filter(id=item['id'])
        for rl in rls:
            rl.mail = item['value']
            rl.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
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
    if req.status_code == 200 or req.status_code == 203:
        return HttpResponse('{"status": "success"}', content_type="application/json")
    else:
        return HttpResponse(status=req.status_code)

@csrf_exempt
def del_hash(request):
    hash_base_id = request.POST['hash_base_id']
    AllHash.objects.filter(hash_base_id=hash_base_id).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def find_active(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    raw_leads = RawLeads.objects.filter(activated=0, date=date)
    for raw_lead in raw_leads:
        drop = raw_lead.name_redemption.split('.')[0]
        zone = raw_lead.name_zone.split('.')[0]
        if drop == zone:
            rl = RawLeads.objects.get(id=raw_lead.id)
            rl.activated = 1
            rl.save()

    return HttpResponse('{"status": "success"}', content_type="application/json")


# SEARCH
@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.user", "domain.admin"]))
def search(request):
    return render(request, 'search.html', {})

@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.user", "domain.admin"]))
def search_results(request):
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

@csrf_exempt
def send_pending(request):
    potential_profits = RawLeads.objects.filter(activated__gte=1, mail__isnull=False, reminder=0)

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
            while req.status_code == 204:
                hash_base_id = binascii.hexlify(os.urandom(16))

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
                    # AllHash.objects.filter(hash_base_id=potential_profit.hash_base_id).update(hash_base_id=hash_base_id)
                als = AllHash.objects.filter(hash_base_id=potential_profit.hash_base_id)
                for al in als:
                    al.hash_base_id = hash_base_id
                    al.save()
                    # RawLeads.objects.filter(id=potential_profit.id).update(reminder=1, hash_base_id=hash_base_id, last_email_date=timezone.now())
                rls = RawLeads.objects.filter(id=potential_profit.id)
                for rl in rls:
                    rl.reminder = 1
                    rl.hash_base_id = hash_base_id
                    rl.last_email_date = timezone.now()
                    rl.save()

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

                    if not Log.objects.filter(date=potential_profit.date).exists():
                        Log(date=potential_profit.date).save()
                    number_of_old_2 = Log.objects.get(date=potential_profit.date).number_sent_2
                    # Log.objects.filter(date=potential_profit.date).update(number_sent_2=(1 + int(number_of_old_2)))
                    ls = Log.objects.filter(date=potential_profit.date)
                    for l in ls:
                        l.number_sent_2 = (1 + int(number_of_old_2))
                        l.save()

                except SMTPServerDisconnected:
                    connection = mail.get_connection()
                    connection.open()
                    connection.send_messages(emails)
        except:
            return HttpResponse(traceback.format_exc(), content_type='application/json')
    connection.close()

    if not Log.objects.filter(date=datetime.now().date()).exists():
        Log().save()
    number_of_old = Log.objects.get(date=datetime.now().date()).number_sent
    # Log.objects.filter(date=datetime.now().date()).update(number_sent=(int(asdi) + int(number_of_old)))
    ls = Log.objects.filter(date=datetime.now().date())
    for l in ls:
        l.number_sent = (int(asdi) + int(number_of_old))
        l.save()

    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def whois_period(request):
    interval = int(request.POST['interval'])
    mode = request.POST['mode']
    dates = []
    for i in range(0, interval):
        date = (datetime.now() - timedelta(days=i)).date()
        dates.append(date)
    main_period(dates, mode)
    return HttpResponse('{"status": "success"}', content_type="application/json")

@user_passes_test(lambda u: any(u.has_perm(perm) for perm in ["domain.admin"]))
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
            'total_a': len(RawLeads.objects.filter(date=date, activated__gte=1)),
            'exceptions': DomainException.objects.all(),
            'tlds': Tlds.objects.all()
        })

@login_required
def removeUnwanted(request):
    removeStuff()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def deleteException(request):
    id_ = request.POST['id']
    DomainException.objects.filter(id=id_).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def addException(request):
    domain = request.POST['name']
    DomainException(domain=domain).save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def deleteTld(request):
    id_ = request.POST['id']
    Tlds.objects.filter(id=id_).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def addTld(request):
    extension = request.POST['name']
    Tlds(extension=extension).save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
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

@csrf_exempt
def Chart(request):
    total = []
    succeeded = []
    total2 = []
    succeeded2 = []
    total3 = []
    succeeded3 = []

    master_of_indexes = 1
    who_analytics = WhoisAnalytics.objects.filter(source="internal").order_by('-id')[0:100]
    for entry in who_analytics:
        total.append({
            "x": int(master_of_indexes),
            "y": int(entry.total)
        })

        succeeded.append({
            "x": int(master_of_indexes),
            "y": int(entry.succeeded)
        })
        master_of_indexes += 1

    master_of_indexes = 1
    who_analytics = WhoisAnalytics.objects.filter(source="external").order_by('-id')[0:100]
    for entry in who_analytics:
        total2.append({
            "x": int(master_of_indexes),
            "y": int(entry.total)
        })

        succeeded2.append({
            "x": int(master_of_indexes),
            "y": int(entry.succeeded)
        })
        master_of_indexes += 1

    master_of_indexes = 1
    who_analytics = WhoisAnalytics.objects.filter(source="he_net").order_by('-id')[0:100]
    for entry in who_analytics:
        total3.append({
            "x": int(master_of_indexes),
            "y": int(entry.total)
        })

        succeeded3.append({
            "x": int(master_of_indexes),
            "y": int(entry.succeeded)
        })
        master_of_indexes += 1

    return render(
        request,
        'charts.html',
        {
            "total": total,  "succeeded": succeeded,
            "total2": total2,  "succeeded2": succeeded2,
            "total3": total3,  "succeeded3": succeeded3,
        })

@csrf_exempt
def whoisHeNet(request):
    if 'date' in request.POST.keys():
        arg = request.POST['date']
    else:
        arg = 'none'

    s = Setting.objects.get(id=1)
    s.run = 1
    s.date = arg
    s.save()

    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def mark_to_active(request):
    if 'date' in request.POST.keys():
        date = datetime.strptime(request.POST['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now().date()

    if 'list_no' in request.POST.keys():
        list_no = int(request.POST['list_no'])
    else:
        list_no = 1

    RawLeads.objects.filter(date=date, list_no=list_no).update(mark=1)
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def un_mark_to_active(request):
    if 'date' in request.POST.keys():
        date = datetime.strptime(request.POST['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now().date()

    if 'list_no' in request.POST.keys():
        list_no = int(request.POST['list_no'])
    else:
        list_no = 1

    RawLeads.objects.filter(date=date, list_no=list_no).update(mark=0)
    return HttpResponse('{"status": "success"}', content_type="application/json")


def saveZoneFiles(request):
    com = request.POST['com'].replace('C:\\fakepath\\', '')
    net = request.POST['net'].replace('C:\\fakepath\\', '')
    org = request.POST['org'].replace('C:\\fakepath\\', '')
    info = request.POST['info'].replace('C:\\fakepath\\', '')
    us = request.POST['us'].replace('C:\\fakepath\\', '')
    biz = request.POST['biz'].replace('C:\\fakepath\\', '')
    mobi = request.POST['mobi'].replace('C:\\fakepath\\', '')

    zones = [
        {'com': com},
        {'net': net},
        {'org': org},
        {'info': info},
        {'us': us},
        {'biz': biz},
        {'mobi': mobi},
    ]

    for zone in zones:
        keys = zone.keys()
        for key in keys:
            z = ZoneFiles.objects.get(zone_type=key)
            z.zone_name = zone[key]
            z.save()

    return HttpResponse('{"status": "success"}', content_type="application/json")
