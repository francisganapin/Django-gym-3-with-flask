from django.contrib import admin
from django.urls import path, include
from . import views  # Adjust this to import your views correctly

urlpatterns = [
    path('member-list/', views.member_list_view, name='member_list_view'),
    path('member-register/', views.member_register_view, name='member_register_view'),
    path('member_update_views/',views.member_update_views,name='member_update_views')
]
