"""DomainScript URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import domain.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #  editing
    url(r'^$', domain.views.editing),
    url(r'^run_script/', domain.views.runEditing),
    #  raw leads
    url(r'^raw_leads/', domain.views.rawLeads),
    url(r'^reverse_state/', domain.views.reverse_state),
    url(r'^find_mails/', domain.views.find_mails),
    url(r'^truncate/', domain.views.truncate),
    url(r'^select_all/', domain.views.select_all),
    url(r'^add_this_name/', domain.views.add_this_name),
    url(r'^rem_this_name/', domain.views.rem_this_name),
    #  active leads
    url(r'^active_leads/', domain.views.activeLeads),
    url(r'^blacklist/', domain.views.blacklist),
    url(r'^blacklist_selected/', domain.views.blacklist_selected),
    url(r'^mark_to_send/', domain.views.mark_to_send),
    url(r'^un_mark_to_send/', domain.views.un_mark_to_send),
    url(r'^delete/', domain.views.delete),
    url(r'^send_mails/', domain.views.send_mails),
    url(r'^add_mail_man/', domain.views.add_mail_man),
    url(r'^rem_mail/', domain.views.rem_mail),
    #  super blaklist 
    url(r'^blacklisting/', domain.views.blacklisting),
    url(r'^super_blacklist/', domain.views.super_blacklist),
    url(r'^regular_blacklist/', domain.views.regular_blacklist),
    url(r'^remove_from_blacklist/', domain.views.remove_from_blacklist),
]
