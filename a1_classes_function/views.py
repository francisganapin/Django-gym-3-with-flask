#Django Import
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

#import for our database
import pymongo

#standard library
import requests

#List of function we use
from global_function import GlobalFunction

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

        class_id = request.GET.get('id_card')
        class_name = request.GET.get('query_name')

        if class_id:
            classes_data = [x for x in classes_data if class_id in str(x.get('class_id_card',''))]

        if class_name:
            classes_data = [x for x in classes_data if class_name.lower() in str(x.get('name','')).lower()]

        paginator = Paginator(classes_data,5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)



    except Exception as e:
        print(f"error: {e}")
        return render(request, 'error.html')

    context ={
        'classes_data':page_obj
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

    api_url_class = 'http://127.0.0.1:5000/api/class/option' # we should run our flask server before we can access this
    api_url_trainor = 'http://127.0.0.1:5000/api/trainor/list'  
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

        random_id = GlobalFunction.generate_random_id()
    except Exception as e:
        print(f'error: {e}')
        return render(request,'error.html')

    context = {
            'class_data_option':class_data_option,
            'trainor_data_option':trainor_data_option,
            'random_id':random_id
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

