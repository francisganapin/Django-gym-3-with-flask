from flask import Flask,jsonify,Response 
import json
from pymongo_server import ConnectionMongoDB


app = Flask(__name__)


db_connection = ConnectionMongoDB()
member_collection = db_connection.get_collection('member_list')




@app.route('/api/members/2',methods=['GET'])
def show_member():
    user = list(member_collection.find({},{'_id':0}))
    return jsonify(user),200




if __name__ == '__main__':
    app.run(debug=True)