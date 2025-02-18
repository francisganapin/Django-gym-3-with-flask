from django.shortcuts import render, redirect
import requests
from django.core.paginator import Paginator
import logging
import datetime
from datetime import datetime
# Create your views here.
# Create your views here.\
import pymongo
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render
from django.http import JsonResponse
import requests

def class_list_view(request):
    api_url_class = 'http://127.0.0.1:5000/api/class/list'
    
    try:
        response = requests.get(api_url_class)
        response.raise_for_status()
        classes_data = response.json()
    except Exception as e:
        print(f"error: {e}")
        return render(request, 'error.html')

    context ={
        'classes_data':classes_data
    }
    return render(request,'classes/classes_list.html',context)