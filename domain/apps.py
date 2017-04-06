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

    subject = 'Acquire' + domain_name + ' With Your Own Offer. Get 25,000 Traffic/Month'
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

    subject = 'Acquire' + domain_name + ' Be Google Friendly and Increase Visibility'
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

    subject = domain_name + ' - Be Visible With a SEO Domain | Experience Traffic Soar'
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

    subject = domain_name + ' - Your Customers Click on Names they can Trust. Increase Traffic + Sales With The Right Domain'
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

def form_a_msg6(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Get Your Domain An Upgrade | Use The #1 Traffic Hack to Increase Website Visitors'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template6.html', 'r')
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

def form_a_msg7(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Available For The First Time Since You Last Checked'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template7.html', 'r')
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

def form_a_msg8(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = 'Upgrade Your Domain to ' + domain_name
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template8.html', 'r')
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

def form_a_msg9(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = domain_name + ' Steal Traffic | Increase Organic Views upto 400% With This Premium Name'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template9.html', 'r')
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

def form_a_msg10(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Increase Traffic By Over 100% In Less Than 30 Days'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template10.html', 'r')
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


# REMINDERS
def pr_msg1(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()
    subject = domain_name + '- Available shortly - Increase targeted traffic to your site'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template1r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def pr_msg2(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()

    subject = domain_name + '- Will Make Your Site  Googles Best Friend'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template2r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def pr_msg3(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Traffic Overload Is On It\'s Way'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template3r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def pr_msg4(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Grab yourself this SEO enhancer'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template4r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def pr_msg5(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Secure This Name For Major Traffic Overload'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template5r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def pr_msg6(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()

    subject = 'Get ' + domain_name + ' - Trouble Getting Traffic? Problem Solved!'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template6r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def pr_msg7(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Increase visibility and attract quality traffic'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template7r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]


def pr_msg8(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Get targeted traffic without spending on ads'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template8r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def pr_msg9(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()

    subject = domain_name + ' - There is nothing called \'Too Much Traffic\''
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template9r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def pr_msg10(domain_name, name, link_un, link_offer):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Boost traffic, get more leads, more revenue. Simple.'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/template10r.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'link_un': link_un,
            'link_offer': link_offer,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]
