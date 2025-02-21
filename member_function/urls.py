from django.contrib import admin
from django.urls import path, include
from . import views  # Adjust this to import your views correctly


urlpatterns = [
    path('member-list/', views.member_list_view, name='member_list_view'),
    path('member-list/<str:member_id>/<str:first_name>/<str:last_name>/<str:expiry>',views.member_list_view_update,name='member_list_view_update'),
    path('member_login_view/',views.member_login_view,name='member_login_view'),
    path('member-register/', views.member_register_view, name='member_register_view'),
    path('member_update_views/',views.member_update_views,name='member_update_views'),
    path('member-list/export',views.some_view,name='some_view')
]
