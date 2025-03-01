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


class ClassFunction:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['gym_system_db']
    collection = db['class_list']

class TrainorDatabase:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['gym_system_db']
    collection = db['trainor_list']

def class_list_view(request):
    api_url_class = 'http://127.0.0.1:5000/api/class/list' # get api address so we can fetch this on our django
    
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


def delete_item_view(request,class_id_card):

    if request.method == 'POST':
        data = {'class_id_card':class_id_card}

    try:
        ClassFunction.collection.delete_one(data)
        return redirect('class_list_view')
    except pymongo.errors.DuplicateKeyError:
        message = f'Member ID Card was not exist {data}'
        return render(request, 'classes/classes_register.html',{'message':message})
    





def class_register_view(request):

    api_url_class = 'http://127.0.0.1:5000/api/class/option'
    api_url_trainor = 'http://127.0.0.1:5000/api/trainor/list'
    response_class = ''
    archive = False # we use this to automatically false the creation
    try:
        #trainor list option
        response_trainor = requests.get(api_url_trainor)
        response_trainor.raise_for_status()
        trainor_data_option =response_trainor.json()

        #class list option
        response_class = requests.get(api_url_class)
        response_class.raise_for_status()
        class_data_option = response_class.json()

     
    except Exception as e:
        print(f'error: {e}')
        return render(request,'error.html')

    
    context = {
            'class_data_option':class_data_option,
            'trainor_data_option':trainor_data_option
        }
        
    if request.method == 'POST':
        name = request.POST.get('name')
        class_id_card = request.POST.get('class_id_card')
        instructor = request.POST.get('instructor')
        duration = request.POST.get('duration')
        schedule = request.POST.get('schedule')

           
        data = {
            "name": name,
            "class_id_card":class_id_card, 
            "instructor":instructor,
            "duration":duration, 
            "schedule": schedule,
            'archive':archive
            }

        try:
            ClassFunction.collection.insert_one(data)
            return redirect('class_list_view')
        except pymongo.errors.DuplicateKeyError:
            message = f'Member ID Card was already exist {class_id_card}'
            return render(request, 'classes/classes_register.html',{context})

    return render(request, 'classes/classes_register.html',context) 

