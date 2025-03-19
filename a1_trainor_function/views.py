#Django Import
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

#Standard import
import requests

#import for database
import pymongo

#List of function we use
from global_function import GlobalFunction


class TrainorClass:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['gym_system_db']
    collection = db['trainor_list']





# Create your views here.
def trainor_list_view(request):
    """Get trainor list and fetch it as view"""

    api_url_data = 'http://127.0.0.1:5000/api/trainor/list'# we should run our flask server before we can access this
    response = ''
    try:
        response = requests.get(api_url_data)
        response.raise_for_status()
        posts = response.json() if isinstance(response.json(),list) else []


        trainer_id = request.GET.get('id_card')
        trainor_name = request.GET.get('query_name')
        # we use this code to get queary as list on member.get('id_card') we find id card dont add this
            
        if trainer_id:
            posts = [member for member in posts if trainer_id in str(member.get('trainer_id', ''))]
        
        # search name of member
        if trainor_name:
            posts = [member for member in posts if trainor_name in str(member.get('first_name', '') + member.get('last_name', ''))]

        paginator = Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        print(response)
    except:
        print('sorry api provider was not working this time')
        return render(request,'error.html')
    return render (request,'trainor/trainor_list.html',{'trainor_list':page_obj})


def trainor_register_view(request):
    api_url_class = 'http://127.0.0.1:5000/api/class/option' # we should run our flask server before we can access this

    #class list option
    response_class = requests.get(api_url_class)
    response_class.raise_for_status()
    class_data_option = response_class.json()

    # random id generator for our auto creat id
    random_id = GlobalFunction.generate_random_id()

    if request.method == 'POST':
        
        trainer_id  = request.POST.get('trainer_id')
        first_name  = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        birthday  = request.POST.get('birthday')
        specialty  = request.POST.get('specialty') 
        phone_number  = request.POST.get('phone_number')
        rate  = request.POST.get('rate')
        percentage  = request.POST.get('percentage')

        data = {
                    'trainer_id':trainer_id,
                    'first_name':first_name,
                    'last_name':last_name,
                    'birthday':birthday,
                    'specialty':specialty,
                    'phone_number':phone_number,
                    'rate':rate,
                    'percentage':percentage
        }
        try:
            TrainorClass.collection.insert_one(data)
            return redirect('trainor_list_view')
        except pymongo.errors.DuplicateKeyError:
                message = f'Member ID Card was already exist {trainer_id}'
                return render(request, 'trainor/trainor_register.html',{'message':message})
        
    return render(request, 'trainor/trainor_register.html',{'class_data_option':class_data_option,'random_id':random_id})