from flask import Flask,jsonify,Response 
import json


app = Flask(__name__)

# Load the JSON data
input_file = "member.json"
with open(input_file, encoding="utf-8") as json_file:
    parsed_json = json.load(json_file)


@app.route('/api/members/2',methods=['GET'])
def show_member():
    user= parsed_json
    return jsonify(user)




if __name__ == '__main__':
    app.run(debug=True)