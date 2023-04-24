from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/identity/login')
def index_view(request):
    return render(request, "index.html", {})
