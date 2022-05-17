import hashlib
import json
import jwt
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

SECRET_KEY = 'turtle'

app = Flask(__name__)
cors = CORS(app, resources={r'*': {'origins': '*'}})
client = MongoClient('localhost', 27017)
db = client.turtlegram

@app.route("/")
def hello_word():
    return jsonify({'msg':'success'})

@app.route("/signup", methods=["POST"])
def sign_up():
    
    data = json.loads(request.data)
    
    password_hash = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
    
    doc = {
        'email' : data.get('email'),
        'password' : password_hash
    }
    
    db.users.insert_one(doc)
    
    return jsonify({'msg':'success'})


@app.route("/login", methods=["POST"])
def login():
    print(request)
    data = json.loads(request.data)
    print(data)
    
    email = data.get("email")
    password = data.get("password")
     # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(hashed_pw)
    
    result = db.users.find_one({
        'email': email, 
        'password': hashed_pw
    })
    
    if result:
        print(result)
       
        
        payload = {
            'id': str(result["_id"]),
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256')
        print(payload)
        print(token)
    
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    
    
    
    



if __name__ =='__main__':
    app.run('0.0.0.0', port=5000, debug=True)