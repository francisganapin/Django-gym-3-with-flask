from django.contrib import admin
from django.urls import path, include
from . import views  # Adjust this to import your views correctly


urlpatterns = [
    path('payment/views', views.payment_members_views, name='payment_function'),
]


