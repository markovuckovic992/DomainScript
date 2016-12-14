from __future__ import unicode_literals

from django.apps import AppConfig


class DomainConfig(AppConfig):
    name = 'domain'


def form_a_msg1(domain_name, link, unsubscribe):  
    domain_name = domain_name.upper() 
    line_offer = "<a href='" + str(link) + "'>OFFER PAGE LINK</a>"
    link_un = "<a href='" + unsubscribe + "'>[LINK]</a>"

    subject = domain_name + ' Get more traffic, more leads, more sales. Simple'
    msg =  'Hi,'  
    msg += '<br/>'
    msg += 'I just wanted to drop a line to let you know that the domain ' + domain_name + ' will shortly be up for sale. If you are interested, you can grab this keyword-rich premium domain for the right offer.'  
    msg += '<br/>' 
    msg += 'Premium domains come with a host of advantages to boost SEO campaigns. They even receive higher CTRs (Click Through Rate) than freshly registered new domains. ' 
    msg += '<br/>' 
    msg += 'To acquire this domain, please click on the link below and make an offer or, simply reply back to this email with your offer: ' 
    msg += '<br/>' 
    msg += line_offer 
    msg += '<br/>' 
    msg += 'Just like you, we take SEO and traffic seriously. ' 
    msg += '<br/>' 
    msg += 'If you have any questions or need any help, please do not hesitate to ask. ' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += 'Best regards' 
    msg += '<br/>' 
    msg += 'Unsubscribe here - ' + link_un

    return [subject, msg]

def form_a_msg2(domain_name, link, unsubscribe): 
    domain_name = domain_name.upper() 
    line_offer = "<a href='" + str(link) + "'>OFFER PAGE LINK</a>"
    link_un = "<a href='" + unsubscribe + "'>[LINK]</a>"

    subject = domain_name + ' Available shortly - Increase targeted traffic to your site'
    msg =  'Hi,'  
    msg += '<br/>'
    msg += 'I just wanted to remind you know that the domain ' + domain_name + ' will shortly be up for sale. If you are interested, you can grab this keyword-rich premium domain for the right offer.'  
    msg += '<br/>' 
    msg += 'Premium domains come with a host of advantages to boost SEO campaigns. They even receive higher CTRs (Click Through Rate) than freshly registered new domains. ' 
    msg += '<br/>' 
    msg += 'To acquire this domain, please click on the link below and make an offer or, simply reply back to this email with your offer: ' 
    msg += '<br/>' 
    msg += line_offer 
    msg += '<br/>' 
    msg += 'Just like you, we take SEO and traffic seriously. ' 
    msg += '<br/>' 
    msg += 'If you have any questions or need any help, please do not hesitate to ask. ' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += 'Best regards' 
    msg += '<br/>' 
    msg += 'Unsubscribe here - ' + link_un

    return [subject, msg]

def form_a_msg3(domain_name, link, unsubscribe):  
    domain_name = domain_name.upper() 
    line_offer = "<a href='" + str(link) + "'>OFFER PAGE LINK</a>"
    link_un = "<a href='" + unsubscribe + "'>[LINK]</a>"

    subject = domain_name + ' Available soon - More targeted traffic, more warm leads'
    msg =  'Hi,'  
    msg += '<br/>'
    msg += 'I wanted to bring to your attention that ' + domain_name + ' will be available shortly. This is a Google indexed premium domain. Premium domains are great for all those who are serious about online traffic as they drive targeted organic traffic to your site.'  
    msg += '<br/>' 
    msg += 'Once the domain is gone, it is gone for good. To grab this domain and get full ownership, visit us by following the link below. ' 
    msg += '<br/>' 
    msg += line_offer 
    msg += '<br/>' 
    msg += 'Need any help? Please feel free to contact our friendly customer support team. Simply reply back to this email. ' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += 'Best wishes' 
    msg += '<br/>' 
    msg += 'Unsubscribe here - ' + link_un

    return [subject, msg]

def form_a_msg4(domain_name, link, unsubscribe):  
    domain_name = domain_name.upper() 
    line_offer = "<a href='" + str(link) + "'>OFFER PAGE LINK</a>"
    link_un = "<a href='" + unsubscribe + "'>[LINK]</a>"

    subject = domain_name + ' Available soon, More targeted traffic, more warm leads'
    msg =  'Hi,'  
    msg += '<br/>'
    msg += domain_name + ' will be available shortly and I wanted to check if you would be interested since you have a very similar domain. '  
    msg += '<br/>' 
    msg += 'Aged premium domains like this are great for high ranking as they are indexed by all major search engines. ' 
    msg += '<br/>' 
    msg += 'Want to secure this domain before it is gone? Simply visit us following the link below and make an offer. ' 
    msg += '<br/>' 
    msg += line_offer 
    msg += '<br/>' 
    msg += 'Not sure how it works? Visit our FAQs page to see how simply you can acquire this domain, it is really as simple as 1-2-3. ' 
    msg += '<br/>' 
    msg += 'If you still need help, then we are here for you. Simply drop us a line or write to us in reply to this email and we will get back to you. ' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += '<br/>' 
    msg += 'Best wishes' 
    msg += '<br/>' 
    msg += 'Unsubscribe here - ' + link_un

    return [subject, msg]