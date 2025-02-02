from django.urls import path
from . import views

urlpatterns = [
    path('gym_member_lis', views.gym_member_list, name='gym_member_lis'),
]