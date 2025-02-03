from django.shortcuts import render
import requests
from django.core.paginator import Paginator
import logging
# Create your views here.
# Create your views here.
def member_list_view(request):
    api_url_member = 'http://127.0.0.1:5000/api/members/list'
    response = ''


    try:
        response = requests.get(api_url_member,timeout=5)
        response.raise_for_status()
        posts = response.json() if isinstance(response.json(),list) else []
    except:
        print(f"sorry your api provider was not working this time")
        return render(request,'error.html')

    context = {
        'member_list':posts
    }
    return render(request, 'member/member_list.html', context)




