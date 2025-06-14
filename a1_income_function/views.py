from django.shortcuts import render,redirect
import datetime

import pymongo
import pymongo.errors

class PaymentDatabase:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['gym_system_db']
    collection = db['income_list']

def payment_members_views(request):

    if request.method =='POST':
        member_id = request.POST.get('member_id')
        amount = request.POST.get('amount')
        payment_date = datetime.datetime.now()
        status = request.POST.get('status')
        receipt_number = request.POST.get('receipt_number')

        data = {
            'member_id':member_id,
            'amount':amount,
            'payment_date':payment_date,
            'status':status,
            'receipt_number':receipt_number,
        }        
  
        PaymentDatabase.collection.insert_one(data)
    return render(request,'income/payment.html')