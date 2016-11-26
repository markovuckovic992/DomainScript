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
    url(r'^active_leads/', domain.views.sending),
    url(r'^blacklist/', domain.views.blacklist),
    url(r'^mark_to_send/', domain.views.mark_to_send),
    #  filtering
    url(r'^raw_leads/', domain.views.filtering),
    url(r'^reverse_state/', domain.views.reverse_state),
    url(r'^mark_for_archive/', domain.views.mark_for_archive),
    url(r'^send_mails/', domain.views.send_mails),
    url(r'^find_mails/', domain.views.find_mails),
    #  deleting
    url(r'^restore/', domain.views.deleting),
    url(r'^delete/', domain.views.delete),
    url(r'^return_from_archive/', domain.views.returnFromArchive),
    url(r'^do_deleting/', domain.views.doDeleting),
    #  sent
    url(r'^sent/', domain.views.sent),
    #  offer
    url(r'^offers/', domain.views.offers),
    url(r'^contact/', domain.views.contact),
    url(r'^process_offer/', domain.views.process_offer),
    # url(r'^find_status/', domain.views.find_status),
]
