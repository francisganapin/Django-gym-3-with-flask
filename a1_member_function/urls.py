from django.contrib import admin
from django.urls import path, include
from . import views  # Adjust this to import your views correctly
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('member-list/', views.member_list_view, name='member_list_view'),
    path('member-list/<str:id_card>',views.archive_member_view,name='archive_member_view'),
    path('member-list/<str:member_id>/<str:first_name>/<str:last_name>/<str:expiry>',views.member_list_view_update,name='member_list_view_update'),
    path('member_login_view/',views.member_login_view_function,name='member_login_view'),
    path('member-register/', views.member_register_view, name='member_register_view'),
    path('member_update_views/',views.member_update_views,name='member_update_views'),
    path('member-list/list/export',views.export_view,name='export_view'),
    path('member/login/list',views.member_login_list_view,name='member_login_list_view'),

    # this will update member_expiry on member list
    path('member/update/<str:member_id>/',views.update_member_list_expiry,name='update_member_list_expiry'),

    #this will register a member inside member_list_view
    path('register/member/list/view',views.register_member_list_view,name='register_member_list_view')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

