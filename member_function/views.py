from django.shortcuts import render
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# Create your views here.
def member_list_view(request):
    response = requests.get('http://127.0.0.1:5000/api/members/2')

    if response.status_code == 200:
        posts = response.json()
    else:
        posts = []

    paginator = Paginator(posts,10)  # Show 10 users per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj
    }
    return render(request, 'member_list.html', context)


