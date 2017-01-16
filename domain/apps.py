from __future__ import unicode_literals
from django.apps import AppConfig
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, Template
from django.conf import settings
import codecs


class DomainConfig(AppConfig):
    name = 'domain'


def form_a_msg1(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = domain_name + ' Get more traffic, more leads, more sales. Simple'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template1.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'link_offer': link,
            'link_un': unsubscribe,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]




def form_a_msg2(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = 'Upgrade Your Domain to ' + domain_name
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template2.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'link_offer': link,
            'link_un': unsubscribe,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]


def form_a_msg3(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Get Your Domain An Upgrade'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template3.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'link_offer': link,
            'link_un': unsubscribe,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]


def form_a_msg4(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Available For The First Time Since You Last Checked'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template4.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'link_offer': link,
            'link_un': unsubscribe,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def form_a_msg5(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Increase Traffic By Over 100% In Less Than 30 Days'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template5.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'link_offer': link,
            'link_un': unsubscribe,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]
