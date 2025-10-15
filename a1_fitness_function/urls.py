from django.contrib import admin
from django.urls import path, include
from . import views  # Adjust this to import your views correctly


urlpatterns = [
    path('fitness/function/bmi', views.bmi_calculator, name='bmi_calculator'),
    path('fitness/function/bmr', views.bmr_calculator, name='bmr_calculator')
  
]
