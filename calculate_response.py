import timeit
import django
from django.test import RequestFactory
from a1_member_function.views import member_list_view
from a1_dashboard.views import dashboard_views
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_app_5.settings')
django.setup()

factory = RequestFactory()
request = factory.get('')

execution_time = timeit.timeit(lambda:dashboard_views(request),number = 10) /10
print({execution_time})