from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from django.core.paginator import Paginator
import pymongo


import secrets
import string

class TrainorClass:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['gym_system_db']
    collection = db['trainor_list']




def generate_random_id(length=8):
    length = 8
    random_string = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
    return ''.join(random_string)



# Create your views here.
def trainor_list_view(request):
    api_url_data = 'http://127.0.0.1:5000/api/trainor/list'
    response = ''
    try:
        response = requests.get(api_url_data)
        response.raise_for_status()
        posts = response.json() if isinstance(response.json(),list) else []


        trainer_id = request.GET.get('trainer_id')
        query_gender = request.GET.get('gender')

        # we use this code to get queary as list on member.get('id_card') we find id card dont add this

        #if queary_card:
            #posts = [member for member in posts if queary_card in str(member.get('member', {}).get('id_card', ''))]
          
        
        #if queary_gender:
            #posts = [member for member in posts if queary_gender in str(member.get('gender', {}).get('gender',''))]
            
        if trainer_id:
            posts = [member for member in posts if trainer_id in str(member.get('trainer_id', ''))]

        paginator = Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        print(response)
    except:
        print('sorry api provider was not working this time')
        return render(request,'error.html')
    return render (request,'trainor/trainor_list.html',{'trainor_list':page_obj})


def trainor_register_view(request):
    api_url_class = 'http://127.0.0.1:5000/api/class/option'

    #class list option
    response_class = requests.get(api_url_class)
    response_class.raise_for_status()
    class_data_option = response_class.json()

    random_id = generate_random_id()

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