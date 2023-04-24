from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_view),
    path('scan', views.scan_view),
    path('details', views.details_view),
    path('ajax', views.ajax, name='ajax'),
]