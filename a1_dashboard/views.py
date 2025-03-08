#Django import
from django.shortcuts import render
from django.core.paginator import Paginator

import requests

def dashboard_views(request):
    api_url_member_count = 'http://127.0.0.1:5000/api/dashboard/' # we should run our flask server before we can access this
    response_data = []

    try:
        response = requests.get(api_url_member_count, timeout=5)
        response.raise_for_status()
        response_data = response.json() 
        print(response_data)

        
    except requests.exceptions.RequestException as e:
        print(e)
        return render(request, 'error.html')

    context = {'response': response_data}
    print(context)
    return render(request, 'dashboard/dashboard.html', context)


