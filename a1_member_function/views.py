#Django imports
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

#standard library import
from datetime import datetime
import csv
import requests

#third party import for pymongo
import pymongo

#List of function we use
from global_function import GlobalFunction



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
  

     # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['gym_system_db']
    collection = db['member_list']

                # Ensure unique ID card
    collection.create_index([('id_card', pymongo.ASCENDING)], unique=True)

    # this code is for profile image request it will save on our destination
    def upload(request):
        folder = 'media/image'
        if request.method == 'POST' and request.FILES['profile_image']:
            myfile = request.FILES['profile_image']
            fs = FileSystemStorage(location=folder)
            filename = fs.save(myfile.name,myfile)
            print(filename)

class LoginClass:
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['gym_system_db']
    collection = db['member_login']


def member_list_view(request):

    #we use this for register
    random_id = GlobalFunction.generate_random_id()

    api_url_member = 'http://127.0.0.1:5000/api/members/list'
    response = ''
    login_date = MemberClass.today.date()
    print(login_date)
    try:
        response = requests.get(api_url_member,timeout=5)
        response.raise_for_status()
    
        posts = response.json() if isinstance(response.json(),list) else []

        #parse date logic we convert api date string to date object
        #for post in posts:
            #post['expiry'] = datetime.strptime(post['expiry'],"%Y-%m-%d")

        #exclude archive true so we can hide the member pass it to flask so it wont show if we search
        post_exclude = [archive for archive in posts if archive['archive'] != True ]

        queary_card = request.GET.get('id_card')
        queary_gender = request.GET.get('gender')
        # we use this code to get queary as list on member.get('id_card') we find id card
        if queary_card:
            post_exclude = [member for member in posts if queary_card in str(member.get('id_card', ''))]
            if not post_exclude:
                post_exclude = [MemberClass.no_data]
        
        if queary_gender:
            post_exclude = [member for member in posts if queary_gender in str(member.get('gender',''))]


        paginator = Paginator(post_exclude,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


    except:
        print(f"sorry your api provider was not working this time")
        return render(request,'error.html')
 
    print(post_exclude)

    context = {
        'member_list':page_obj,
        'login_date':login_date,
        'random_id':random_id
    }
    return render(request, 'member/member_list.html', context)


def member_login_list_view(request):
    api_url_data = 'http://127.0.0.1:5000/api/member/login/history'
    response = ''
    try:
        response = requests.get(api_url_data)
        response.raise_for_status()
        posts = response.json() if isinstance(response.json(),list) else []


        query_card = request.GET.get('id_card')
        query_gender = request.GET.get('gender')

        # we use this code to get queary as list on member.get('id_card') we find id card dont add this

        #if queary_card:
            #posts = [member for member in posts if queary_card in str(member.get('member', {}).get('id_card', ''))]
          
        
        #if queary_gender:
            #posts = [member for member in posts if queary_gender in str(member.get('gender', {}).get('gender',''))]
            
        if query_card:
            posts = [member for member in posts if query_card in str(member.get('member', {}).get('id_card', ''))]
        
        if query_gender:
            posts = [member for member in posts if query_gender in str(member.get('member', {}).get('gender', ''))]

        paginator = Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        print(response)
    except:
        print('sorry api provider was not working this time')
        return render(request,'error.html')
    return render (request,'member/member_login_list.html',{'login_detail':page_obj})
    
def member_list_view_update(request,member_id,first_name,last_name,expiry):

    member_data = {
        'first_name':first_name,
        'last_name':last_name,
        'expiry':expiry
    }
    
     
    print(list(member_data)) # check this for 

    if request.method == 'POST':
        id_card = member_id
        expiry = request.POST.get('expiry')

        queary = { "id_card": { "$regex": id_card } }
        insert = { "$set":{'expiry':expiry}}
    try:
        MemberClass.collection.update_one(queary,insert)
    except:
         print('data was not updated')
    
    return render (request,'member/member_update_list.html',{'member_data':member_data})



def member_login_view_function(request):

    login_date = MemberClass.today
    context = {}
    if request.method == 'POST':
        id_card = request.POST.get('id_card')


        query = {"id_card": id_card }    
       
    try:
        member_data = MemberClass.collection.find_one(query)
        context = {'member':member_data,'login_date':login_date}

        print(login_date)
        print(context['member']['first_name'], context['member']['last_name'],context['member']['expiry'])
        LoginClass.collection.insert_one(context)

    except:
         print('data was not updated')
    
    return render (request,'member/member_login.html',context)

def member_register_view(request):
    
    random_id = GlobalFunction.generate_random_id()

    if request.method == 'POST':
        id_card = request.POST.get('id_card')
        expiry = request.POST.get('expiry')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        join_date = MemberClass.today
        renewed = True
        
        profile_image_path = MemberClass.upload(request)
        data = {
            'id_card':id_card,
            'expiry':expiry,
            'first_name':first_name,
            'last_name':last_name,
            'gender':gender,
            'address':address,
            'phone_number':phone_number,
            'profile_image':profile_image_path,
            'join_date':join_date,
            'renewed':renewed,
            'archive':False
        }

        try:
                MemberClass.collection.insert_one(data)
                return redirect('member_list_view') # if success it wil lgo to member_list_view
        
        except pymongo.errors.DuplicateKeyError:
                message = f'Member ID Card was already exist {id_card}'
                return render(request, 'member/member_register.html',{'message':message})
    
    return render(request, 'member/member_register.html',{'random_id':random_id})


def member_update_views(request):

     
    if request.method == 'POST':
        id_card = request.POST.get('id_card')
        expiry = request.POST.get('expiry')

        queary = { "id_card": { "$regex": id_card } }
        insert = { "$set":{'expiry':expiry}}
    try:
        MemberClass.collection.update_one(queary,insert)
    except:
         print('data was not updated')
    
    return render (request,'member/member_update.html')

#export function
def export_view(request):
    # Create the HttpResponse object with the appropriate CSV header.

    api_url_member = 'http://127.0.0.1:5000/api/members/list'
    response = ''

    response = requests.get(api_url_member)
    data = response.json()
    

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["id_card", "expiry", "first_name", "last_name","gender","phone_number","profile_image","join_date","renewed","archive"])
    for member in data:
        writer.writerow([
            member['id_card'],
            member['expiry'],
            member['first_name'],
            member['last_name'],
            member['gender'],
            member['phone_number'],
            member['profile_image'],
            member['join_date'],
            member['renewed'],
            member['archive']
        ])
    
    return response



def register_button(request):
    # Create the HttpResponse object with the appropriate CSV header.

    api_url_member = 'http://127.0.0.1:5000/api/members/list'
    response = ''

    response = requests.get(api_url_member)
    data = response.json()
    

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["id_card", "expiry", "first_name", "last_name","gender","phone_number","profile_image","join_date","renewed","archive"])
    for member in data:
        writer.writerow([
            member['id_card'],
            member['expiry'],
            member['first_name'],
            member['last_name'],
            member['gender'],
            member['phone_number'],
            member['profile_image'],
            member['join_date'],
            member['renewed'],
            member['archive']
        ])
    
    return response



def archive_member_view(request,id_card):

    if request.method == 'POST':
        data = {'id_card':id_card}
        newvalues = {"$set":{'archive':True}}
    try:
        MemberClass.collection.update_one(data,newvalues)
        return redirect('member_list_view')
    except pymongo.errors.DuplicateKeyError:
        message = f'Member ID Card was not exist {data}'
        return render(request, 'member/member_list.html',{'message':message})
    




#THIS CODE WILL EDIT OUR EXPIRY IN FRONT END
def update_member_list_expiry(request,member_id):
    
    if request.method == 'POST':
        id_card = member_id
        expiry = request.POST.get('expiry')
        
        member_data = {
        'member_id':member_id,
        'expiry':expiry
    }

        if not expiry:
            return HttpResponse("Expiry date is required", status=400)

        queary = { "id_card": { "$regex": id_card } }
        insert = { "$set":{'expiry':expiry}}
    try:
        MemberClass.collection.update_one(queary,insert)
    except:
         print('data was not updated')
    
    return redirect('member_list_view')



def register_member_list_view(request):
    

    if request.method == 'POST':
        id_card = request.POST.get('id_card')
        expiry = request.POST.get('expiry')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        join_date = MemberClass.today
        renewed = True
        
        profile_image_path = MemberClass.upload(request)

        data = {
            'id_card':id_card,
            'expiry':expiry,
            'first_name':first_name,
            'last_name':last_name,
            'gender':gender,
            'address':address,
            'phone_number':phone_number,
            'profile_image':profile_image_path,
            'join_date':join_date,
            'renewed':renewed,
            'archive':False
        }

        try:
                MemberClass.collection.insert_one(data)
                return redirect('member_list_view') # if success it wil lgo to member_list_view
        
        except pymongo.errors.DuplicateKeyError:
                message = f'Member ID Card was already exist {id_card}'
                return render(request, 'member/member_register.html',{'message':message})
    
    return redirect('member_list_view')

