from django.shortcuts import render
from core.section import Section

from core.models import Student
from django.contrib.auth.decorators import login_required

section = Section()
section.actionbar = True
section.breadcrumb = True

@login_required(login_url='/identity/login')
def index_view(request):
    section.page_title = ""
    section.sidebar=False

    mylist = Student.objects.all().order_by('surname')

    context = {
        'section': section,
        'query_string': "",
        'mylist': mylist,
        
    }
    return render(request, 'students/index.html', context)