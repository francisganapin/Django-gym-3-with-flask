from django.shortcuts import render
import requests
import json
def gym_member_list(request):

    response = request.get('http://127.0.0.1:5000/api/members/2')

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f'you are api not connected')
    return render(request,'member_list.html',{'data':data})