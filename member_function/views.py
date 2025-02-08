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

class MemberClass:

    no_data = {
            'id_card': 'No data',
            'first_name': 'No data',
            'last_name': 'No data',
            'address': 'No data',
            'expiry': 'No data',
            'gender': 'No data',
            'join_date': 'No data',
            'phone_number': 'No data',
            'profile_image': 'No data',
            'renewed': 'No data'
            }

    today = datetime.now()
    
    # Format the date as MM-DD-YYYY
    formatted_date = today.strftime("%m-%d-%Y")

     # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['gym_system_db']
    collection = db['member_list']

                # Ensure unique ID card
    collection.create_index([('id_card', pymongo.ASCENDING)], unique=True)
    

def member_list_view(request):

    api_url_member = 'http://127.0.0.1:5000/api/members/list'
    response = ''

    try:
        response = requests.get(api_url_member,timeout=5)
        response.raise_for_status()
        posts = response.json() if isinstance(response.json(),list) else []

        queary_card = request.GET.get('id_card')
        queary_gender = request.GET.get('gender')
        # we use this code to get queary as list on member.get('id_card') we find id card
        if queary_card:
            posts = [member for member in posts if queary_card in str(member.get('id_card', ''))]
            if not posts:
                posts = [MemberClass.no_data]
        
        if queary_gender:
            posts = [member for member in posts if queary_gender in str(member.get('gender',''))]


        paginator = Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


    except:
        print(f"sorry your api provider was not working this time")
        return render(request,'error.html')
 
    print(posts)

    context = {
        'member_list':page_obj
    }
    return render(request, 'member/member_list.html', context)



def member_register_view(request):

    if request.method == 'POST':
        id_card = request.POST.get('id_card')
        expiry = request.POST.get('expiry')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        profile_image = request.FILES.get('profile_image')
        join_date = MemberClass.formatted_date
        renewed = True
        data = {
            'id_card':id_card,
            'expiry':expiry,
            'first_name':first_name,
            'last_name':last_name,
            'gender':gender,
            'address':address,
            'phone_number':phone_number,
            'profile_image':profile_image,
            'join_date':join_date,
            'renewed':renewed
        }

        try:
                MemberClass.collection.insert_one(data)
                return redirect('member_list_view') # if success it wil lgo to member_list_view
        
        except pymongo.errors.DuplicateKeyError:
                message = f'Member ID Card was already exist {id_card}'
                return render(request, 'member/member_register.html',{'message':message})
    
                

    return render(request, 'member/member_register.html')