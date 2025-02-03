from django.shortcuts import render
import requests
from django.core.paginator import Paginator

# Create your views here.
# Create your views here.
def dashboard_views(request):
    api_url_member_count = 'http://127.0.0.1:5000/api/member/count'

    try:
        response = requests.get(api_url_member_count,timeout=5)
        response.raise_for_status()
    except:
        print(response)
        return render(request,'error.html')

    return render(request, 'base.html')


