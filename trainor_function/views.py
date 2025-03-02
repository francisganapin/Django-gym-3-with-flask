from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from django.core.paginator import Paginator


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