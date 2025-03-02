from django.contrib import admin
from django.urls import path, include
from . import views  # Adjust this to import your views correctly


urlpatterns = [
    path('trainor-list/', views.trainor_list_view, name='trainor_list_view'),
   
]
