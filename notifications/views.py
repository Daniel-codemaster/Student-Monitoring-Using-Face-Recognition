from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.models import Notification
from core.section import Section

section = Section()
section.actionbar = True
section.breadcrumb = True

@login_required(login_url='/identity/login')
def index_view(request):
    section.page_title = ""
    section.title = "Notifications"
    section.sidebar=False

    mylist = Notification.objects.all().order_by('creation_date')

    context = {
        'section': section,
        'query_string': "",
        'mylist': mylist,
        
    }
    return render(request, 'notifications/index.html', context)
