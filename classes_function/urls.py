from django.contrib import admin
from django.urls import path, include
from . import views  # Adjust this to import your views correctly


urlpatterns = [
    path('class-list/', views.class_list_view, name='class_list_view'),

]
