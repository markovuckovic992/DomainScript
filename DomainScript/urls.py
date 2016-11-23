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
    #  sending
    url(r'^sending/', domain.views.sending),
    url(r'^blacklist/', domain.views.blacklist),
    url(r'^mark_to_send/', domain.views.mark_to_send),
    #  filtering
    url(r'^filtering/', domain.views.filtering),
    url(r'^reverse_state/', domain.views.reverse_state),
    url(r'^send_mails/', domain.views.send_mails),
    url(r'^find_mails/', domain.views.find_mails),
    #  deleting
    url(r'^deleting/', domain.views.deleting),
    url(r'^return_from_archive/', domain.views.returnFromArchive),
    url(r'^do_deleting/', domain.views.doDeleting),
    #  offers
    url(r'^offers/', domain.views.offers),
]
