from django.contrib import admin
from django.urls import path, include
from . import views  # Adjust this to import your views correctly

urlpatterns = [
    path('', views.member_list_view, name='member_list_view'),
]
