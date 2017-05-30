#!/usr/bin/python
import sys, os, django
from os import popen
os.environ['DISPLAY'] = ':0'
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads, ProcessTracker, SuperBlacklist, DeletedInfo, Emails
from datetime import datetime


import time, traceback
import lxml.html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def whois_he_net(datas):
    vpn_count = 1
    first = True

    browser = webdriver.Chrome('/home/dabset/domains2/Linux/chromedriver')
    # browser = webdriver.Chrome('/home/marko/Linux/chromedriver')
    
    for data in datas:
        # try:
            link = 'http://bgp.he.net/dns/' + data.name_zone + '#_whois'
            browser.get(link)

            time.sleep(1)
            tree = lxml.html.fromstring(browser.page_source)
            time.sleep(1)

            if 'Not Found' not in browser.page_source:
                response = tree.xpath("//div[@id='content']//div[@id='whois']")[0].text_content()

                index = response.find('Registrant Email')
                if index != -1:
                    new = response[index:]
                    response = new.splitlines()[0]
                    email = response.replace('Registrant Email: ', '').replace('\n', '').replace('\r', '')

                if '@' in email:
                    r = RawLeads.objects.get(name_zone=data.name_zone)
                    r.mail = email
                    r.save()

 
                    email = "".join(email.split())
                    blacklisted = BlackList.objects.filter(email__iexact=email)
                    same_shit = ProcessTracker.objects.filter(name_redemption=data.name_redemption, email=email)
                    same_shit_2 = RawLeads.objects.filter(name_redemption=data.name_redemption, mail=email)
                    domain = email.split('@', 1)[1]
                    c_domain = domain.split('.', 1)[0]
                    super_blacklisted = SuperBlacklist.objects.filter(domain=domain)
                    super_same_shit = ProcessTracker.objects.filter(email__endswith='@' + str(domain), name_redemption=data.name_redemption)
                    super_same_shit_2 = RawLeads.objects.filter(mail__endswith='@' + str(domain), name_redemption=data.name_redemption)
                    if blacklisted.exists():
                        record = DeletedInfo(
                            name_zone=data.name_zone,
                            name_redemption=data.name_redemption,
                            date=data.date,
                            email=email,
                            reason='email is blacklisted'
                        )
                        record.save()
                        RawLeads.objects.filter(id=data.id).delete()
                    elif super_blacklisted.exists() and not DomainException.objects.filter(domain=c_domain).exists():
                        record = DeletedInfo(
                            name_zone=data.name_zone,
                            name_redemption=data.name_redemption,
                            date=data.date,
                            email=email,
                            reason='domain is blacklisted'
                        )
                        record.save()
                        RawLeads.objects.filter(id=data.id).delete()
                    elif same_shit.exists() or same_shit_2.exists():
                        record = DeletedInfo(
                            name_zone=data.name_zone,
                            name_redemption=data.name_redemption,
                            date=data.date,
                            email=email,
                            reason='duplicate -- 2'
                        )
                        record.save()
                        RawLeads.objects.filter(id=data.id).delete()
                    elif (super_same_shit.exists() or super_same_shit_2.exists()) and not (DomainException.objects.filter(domain=c_domain).exists() or DomainException.objects.filter(domain=domain).exists):
                        record = DeletedInfo(
                            name_zone=data.name_zone,
                            name_redemption=data.name_redemption,
                            date=data.date,
                            email=email,
                            reason='duplicate domain -- 2'
                        )
                        record.save()
                        RawLeads.objects.filter(id=data.id).delete()
                    else:
                        rl = RawLeads.objects.get(id=data.id)
                        rl.mail = email
                        rl.save()

                        new = ProcessTracker(email=email, name_redemption=data.name_redemption)
                        new.save()
                        if Emails.objects.filter(name_zone=data.name_zone).exists():
                            ems = Emails.objects.filter(name_zone=data.name_zone)
                            for em in ems:
                                em.email = email
                                em.save()
                        else:
                            new = Emails(name_zone=data.name_zone, email=email)
                            new.save()

            else:
                delete = True

        # except:
            # time.sleep(1)
            # if vpn_count == 1:
            #     vpn_count_1 = 3
            # else:
            #     vpn_count_1 = vpn_count - 1

            # if not first:
            #     tube = popen("nmcli con down id 'VPN connection " + unicode(vpn_count_1) + "'")
            #     tube.close()
            # tube = popen("nmcli con up id 'VPN connection " + unicode(vpn_count) + "'")
            # tube.close()
            # vpn_count += 1
            # if vpn_count > 3:
            #     vpn_count = 1

            # first = False

    browser.close()

if __name__ == '__main__':
    if sys.argv[1] != 'none':
        date = sys.argv[1]
        date = datetime.strptime(date, '%d-%m-%Y').date()
        datas = RawLeads.objects.filter(activated__gte=1, mail__isnull=True, date=date).order_by('-id')
    else:
        datas = RawLeads.objects.filter(activated__gte=1, mail__isnull=True).order_by('-id')


    

    whois_he_net(datas)
