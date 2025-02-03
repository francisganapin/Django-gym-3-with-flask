from flask import Flask,jsonify,Response 
import json
from pymongo_server import ConnectionMongoDB
from datetime import datetime

app = Flask(__name__)


db_connection = ConnectionMongoDB()
member_collection = db_connection.get_collection('member_list')


@app.route('/api/dashboard/',methods=['GET'])
def dashbard():
    ''''our dash board will show data here'''

    data_member = member_collection.count_documents({})
    data_renewed_member = member_collection.count_documents({'renewed':True})

    
    

    date_now = datetime.now().strftime("%Y-%m-%d") # date now 

    data_member_expiry = list(member_collection.find({}, {'expiry': 1, '_id': 0}))
    expired_member = [member['expiry']  <= date_now for member in data_member_expiry] # list the expired data  base on date
    count_expired  = expired_member.count(1) # this will count true
    count_active   = expired_member.count(0) # this will count false

    print(f'there is a {count_expired} member that expired today')
    print(expired_member)
    print(date_now)
 
    context = {'data_member':data_member,
                    'data_renewed_member':data_renewed_member,
                    'date_now':date_now,
                    'active_member_count':count_active,
                    'expired_member_count':count_expired
                    }
    
    return jsonify(context),200




@app.route('/api/members/list',methods=['GET'])
def show_member():
    user = list(member_collection.find({},{'_id':0}))
    return jsonify(user),200




if __name__ == '__main__':
    app.run(debug=True)