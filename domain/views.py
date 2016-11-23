from django.shortcuts import render
from django.http import HttpResponse
from urllib import unquote
from domain.models import RawLeads, Offer
from basic_editing import main_filter
from whois_domain import main, main_offer
from django.core.mail import send_mail
from django.conf import settings
from django.db import connection
from datetime import datetime
from os import popen
import requests, hashlib, traceback


def editing(request):
    return render(request, 'editing.html', {})

def runEditing(request):
    try:
        com = request.POST['com']
        net = request.POST['net']
        org = request.POST['org']
        info = request.POST['info']
        redempt = request.POST['redempt']
        date = request.POST['date']
        date = datetime.strptime(date, '%d-%m-%Y').date()
        RawLeads.objects.filter(date=date).delete()
        argument = "pypy /home/dabset/DomainScript/basic_editing.py "
        argument += (com + " " + net + " " + org + " " + info + " ")
        argument += (redempt + " " + str(date))
        popen(argument)
        # main_filter(com, net, org, info, redempt, date)
        return HttpResponse('{"status": "success"}', content_type="application/json")
    except:
        print traceback.format_exc(), argument
        return HttpResponse('{"status": "failed"}', content_type="application/json")

def sending(request):
    if 'date' in request.GET.keys():
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()
    raw_leads = RawLeads.objects.filter(send_mail=1, archive=0, date=date, sent=0)
    return render(request, 'sending.html', {"raw_leads": raw_leads})

def filtering(request):
    if 'date' in request.GET.keys():
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()
    raw_leads = RawLeads.objects.filter(archive=0, date=date, send_mail=0)
    return render(request, 'filtering.html', {"raw_leads": raw_leads})

def reverse_state(request):
    raw_leads_id = int(unquote(request.POST['id']))
    send_mail = RawLeads.objects.get(id=raw_leads_id).send_mail
    send_mail += 1
    send_mail %= 2
    RawLeads.objects.filter(id=raw_leads_id).update(send_mail=send_mail)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def send_mails(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    potential_profits = RawLeads.objects.filter(send_mail=1, sent=0, archive=0, date=date, mark_to_send=1)
    for potential_profit in potential_profits:
        # Form a link

        hash = hashlib.md5()
        hash.update(str(potential_profit.id))
        hash_base_id = hash.hexdigest()
        link = ('http://localhost:8001/offer/?id=' + str(hash_base_id))
        requests.post(
            "http://localhost:8001/add_offer/",
            data={
                'base_id': potential_profit.id,
                'lead': potential_profit.name_redemption,
                'hash_base_id': hash_base_id,
            }
        )
        offer = Offer(
            base_id=potential_profit.id,
            lead=potential_profit.name_redemption,
            zone=potential_profit.name_zone,
            hash_base_id=hash_base_id
        )
        offer.save()
        try:
            send_mail(
                "Domain offer",  # Title
                potential_profit.name_zone,   # Body
                settings.EMAIL_HOST_USER,
                [potential_profit.mail],
                fail_silently=True,
                html_message="<a href='" + str(link) + "'>Link</a>",
            )
            RawLeads.objects.filter(id=potential_profit.id).update(sent=1)
        except:
            pass
    return HttpResponse('{"status": "success"}', content_type="application/json")

def find_mails(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    main(date)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def returnFromArchive(request):
    raw_leads_id = int(unquote(request.POST['id']))
    return_or_delete = RawLeads.objects.get(id=raw_leads_id).return_or_delete
    return_or_delete += 1
    return_or_delete %= 2
    RawLeads.objects.filter(id=raw_leads_id).update(return_or_delete=return_or_delete)
    return HttpResponse('{"status": "success"}', content_type="application/json")


def deleting(request):
    if 'date' in request.GET.keys():
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()
    archive = RawLeads.objects.filter(archive=1, date=date)
    return render(request, 'deleting.html', {"archive": archive})

def doDeleting(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    to_delete = RawLeads.objects.filter(return_or_delete=0, date=date, archive=1)
    to_delete.delete()
    RawLeads.objects.filter(archive=1, date=date).update(archive=0, send_mail=1)
    main(date)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def mark_to_send(request):
    leads_id = int(unquote(request.POST['id']))
    mark_to_send = RawLeads.objects.get(id=leads_id).mark_to_send
    mark_to_send += 1
    mark_to_send %= 2
    RawLeads.objects.filter(id=leads_id).update(mark_to_send=mark_to_send)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def blacklist(request):
    leads_id = int(unquote(request.POST['id']))
    blacklist = RawLeads.objects.get(id=leads_id).blacklist
    blacklist += 1
    blacklist %= 2
    RawLeads.objects.filter(id=leads_id).update(blacklist=blacklist)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def offers(request):
    if 'date' in request.GET.keys():
        date = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
    else:
        date = datetime.now()
    raw_leads = Offer.objects.filter(date=date)
    return render(request, 'offers.html', {"raw_leads": raw_leads})

def check_offer_status(request):
    date = request.POST['date']
    date = datetime.strptime(date, '%d-%m-%Y').date()
    main_offer(date)
    return HttpResponse('{"status": "success"}', content_type="application/json")
