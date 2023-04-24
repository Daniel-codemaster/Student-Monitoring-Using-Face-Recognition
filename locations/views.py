from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.models import Location
from core.section import Section

section = Section()
section.actionbar = True
section.breadcrumb = True

@login_required(login_url='/identity/login')
def index_view(request):
    section.page_title = ""
    section.title = "Locations"
    section.sidebar=False

    mylist = Location.objects.all().order_by('name')

    context = {
        'section': section,
        'query_string': "",
        'mylist': mylist,
        
    }
    return render(request, 'locations/index.html', context)
