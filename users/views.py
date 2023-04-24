from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core.section import Section

section = Section()
section.actionbar = True
section.breadcrumb = True

@login_required(login_url='/identity/login')
def index_view(request):
    section.page_title = ""
    section.title = "Users"
    section.sidebar=False

    mylist = User.objects.all().order_by('username')

    context = {
        'section': section,
        'query_string': "",
        'mylist': mylist,
        
    }
    return render(request, 'users/index.html', context)
