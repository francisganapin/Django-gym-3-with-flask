import timeit
import django
from django.test import RequestFactory
from function.member_function.views import showMember_views

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym.settings')
django.setup()

factory = RequestFactory()
request = factory.get('')

execution_time = timeit.timeit(lambda:showMember_views(request),number = 10) /10
print({execution_time})