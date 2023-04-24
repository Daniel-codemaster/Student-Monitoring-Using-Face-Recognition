from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.section import Section
from core.models import Whatsapp

section = Section()
section.actionbar = True
section.breadcrumb = True

@login_required(login_url='/identity/login')
def index_view(request):
    section.page_title = ""
    section.title = "Whatsapp settings"
    section.sidebar=False

    whatsapp = Whatsapp.objects.first()

    context = {
        'section': section,
        'query_string': "",
        'whatsapp': whatsapp,
        
    }
    return render(request, 'whatsapp_settings/index.html', context)
