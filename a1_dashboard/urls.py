from django.contrib import admin
from django.urls import path, include
from . import views  # Adjust this to import your views correctly
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard_views, name='dashboard_views'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
