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
    # link_offer = "<a href='" + str(link) + "'>OFFER PAGE LINK</a>"
    # link_un = "<a href='" + unsubscribe + "'>[LINK]</a>"

    subject = domain_name + ' Get more traffic, more leads, more sales. Simple'
    # msg = 'Hi,'
    # msg += '<br/><br/>'
    # msg += 'I just wanted to drop a line to let you know that the domain ' + domain_name + ' will shortly be up<br/>'
    # msg += 'for sale. If you are interested, you can grab this keyword-rich premium domain for the right<br/>'
    # msg += '<br/>offer.<br/><br/>'
    # msg += 'Premium domains come with a host of advantages to boost SEO campaigns. They even receive <br/> higher CTRs (Click Through Rate) than freshly registered new domains. <br/><br/>'
    # msg += 'To acquire this domain, please click on the link below and make an offer or, <u>simply reply back to <br/>this email with your offer: </u><br/><br/>'
    # msg += link_offer
    # msg += '<br/><br/>'
    # msg += 'Just like you, we take SEO and traffic seriously. '
    # msg += '<br/><br/>'
    # msg += 'If you have any questions or need any help, please do not hesitate to ask. '
    # msg += '<br/><br/>'
    # msg += '<a style="margin-left: 200px;" href="' + str(link) + '"><img src="http://www.webdomainexpert.pw/static/images/button.png" /></a><br/><br/>'
    # msg += 'Best regards<br/><br/>'
    # msg += 'Unsubscribe here - ' + link_un

    file = codecs.open(settings.EMAIL_TEMPLATES + '/template.html', 'r')
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
    line_offer = "<a href='" + str(link) + "'>OFFER PAGE LINK</a>"
    link_un = "<a href='" + unsubscribe + "'>[LINK]</a>"

    subject = domain_name + ' Available shortly - Increase targeted traffic to your site'
    msg = 'Hi, <br/><br/>'
    msg += 'I just wanted to remind you know that the domain ' + domain_name + ' will shortly be up for sale.<br/>'
    msg += 'If you are interested, you can grab this keyword-rich premium domain for the right offer.<br/><br/>'
    msg += 'Premium domains come with a host of advantages to boost SEO campaigns. They even receive<br/> '
    msg += 'higher CTRs (Click Through Rate) than freshly registered new domains. <br/><br/>'
    msg += 'To acquire this domain, please click on the link below and make an offer or, simply reply back to this email with your offer: '
    msg += '<br/>'
    msg += line_offer
    msg += '<br/><br/>'
    msg += 'Just like you, we take SEO and traffic seriously. '
    msg += '<br/><br/>'
    msg += 'If you have any questions or need any help, please do not hesitate to ask. '
    msg += '<br/><br/>'
    msg += '<a style="margin-left: 200px;" href="' + str(link) + '"><img src="http://www.webdomainexpert.pw/static/images/button.png" /></a><br/><br/>'
    msg += 'Best regards<br/><br/>'
    msg += 'Unsubscribe here - ' + link_un

    return [subject, msg]


def form_a_msg3(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()
    line_offer = "<a href='" + str(link) + "'>OFFER PAGE LINK</a>"
    link_un = "<a href='" + unsubscribe + "'>[LINK]</a>"

    subject = domain_name + ' Available soon - More targeted traffic, more warm leads'
    msg = 'Hi, <br/<br/>'
    msg += 'I wanted to bring to your attention that ' + domain_name + ' will be available shortly. This is a <br/>'
    msg += 'Google indexed premium domain. Premium domains are great for all those who are serious<br/> about online traffic as they drive targeted organic traffic to your site.<br/><br/>'
    msg += 'Once the domain is gone, it is gone for good. To grab this domain and get full ownership, visit us<br/> by following the link below. '
    msg += '<br/><br/>'
    msg += line_offer
    msg += '<br/><br/>'
    msg += 'Need any help? Please feel free to contact our friendly customer support team. Simply reply<br/> back to this email. '
    msg += '<br/><br/>'
    msg += '<a style="margin-left: 200px;" href="' + str(link) + '"><img src="http://www.webdomainexpert.pw/static/images/button.png" /></a>'
    msg += '<br/><br/>'
    msg += 'Best wishes'
    msg += '<br/><br/>'
    msg += 'Unsubscribe here - ' + link_un

    return [subject, msg]


def form_a_msg4(domain_name, link, unsubscribe):
    domain_name = domain_name.upper()
    line_offer = "<a href='" + str(link) + "'>OFFER PAGE LINK</a>"
    link_un = "<a href='" + unsubscribe + "'>[LINK]</a>"

    subject = domain_name + ' Available soon, More targeted traffic, more warm leads'
    msg = 'Hi,'
    msg += '<br/>'
    msg += '<br/>'
    msg += domain_name + ' will be available shortly and I wanted to check if you would be interested since you<br/> have a very similar domain. '
    msg += '<br/><br/>'
    msg += 'Aged premium domains like this are great for high ranking as they are indexed by all major<br/> search engines. '
    msg += '<br/><br/>'
    msg += 'Want to secure this domain before it is gone? Simply visit us following the link below and make<br/> an offer. '
    msg += '<br/><br/>'
    msg += line_offer
    msg += '<br/><br/>'
    msg += 'Not sure how it works? Visit our FAQs page to see how simply you can acquire this domain, it is<br/> really as simple as 1-2-3. '
    msg += '<br/><br/>'
    msg += 'If you still need help, then we are here for you. Simply drop us a line or write to us in reply to<br/> this email and we will get back to you. '
    msg += '<br/><br/>'
    msg += '<a style="margin-left: 200px;" href="' + str(link) + '"><img src="http://www.webdomainexpert.pw/static/images/button.png" /></a>'
    msg += '<br/><br/>'
    msg += 'Best wishes'
    msg += '<br/><br/>'
    msg += 'Unsubscribe here - ' + link_un

    return [subject, msg]
