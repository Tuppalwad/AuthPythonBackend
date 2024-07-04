import string
from system_check.mongo_connection_check import mongo_connection_check
from system_check.redis_connection_check import redis_connection_check
from Email.verify_email import send_verification_link
from Email.Forgot_Password import *
from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_session import Session
import bcrypt
import random
import json
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from config import ApplicationConfig
from flask import jsonify
from Mongo_Connection.connection import Connection
from werkzeug.utils import secure_filename
import time
from common_function import *
from global_variables import BACKEND_URL,APP_URL,mongo_conn_obj,FLASK_PORT,FLASK_DEBUG
from bson.objectid import ObjectId
from datetime import datetime
import pytz

app = Flask(__name__)
app.config.from_object(ApplicationConfig)



# Create and initialize the Flask-Session object AFTER `app` has been configured
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)

@app.route("/register", methods=["POST"])
def register():
    
    data = request.get_json()
    email = data.get("email", False)
    verify_key = data.get('verify_key', False)
    verify_db = mongo_conn_obj.get_mongodb_connection().verify_link
    user_db = mongo_conn_obj.get_mongodb_connection().user

    if not valid_email(email):
        return return_error(error="INVALID_EMAIL", message="invalid email")

    existing_user = user_db.find_one({'email': email})
    if existing_user:
        return return_error(error="USER_ALREADY_EXIST")

    if email and not verify_key:
        # add entry in verify link table
        code = generate_random_string(12)
        new = verify_db.insert_one({'email': email, 'code': code, 'type': 'register'})
        # send verification link
        link = BACKEND_URL + "/email_verify?code=" + code
        sent = send_verification_link(to_email=email, link=link)
        if sent:
            data = {
                "message": "verification mail is sent",
                "email": email
            }
            return return_success(data=data)
        else:
            return return_error()

    else:
        password = data.get("password", False)
        name = data.get('name', False)
        if email and verify_key and password and name:
            # check verify_key
            verify_data = verify_db.find_one({"email": email, "code": verify_key})
            if verify_data:
                # inset data
                hashpass = bcrypt.generate_password_hash(password)
                new = user_db.insert_one({'email': email, 'password': hashpass, 'name': name, "user_type": "FOUNDER",
                                          'setting': {'timezone': 'Asia/Kolkata'}})
                verify_db.delete_one({"email": email, "code": verify_key})
                session['email'] = email
                data = {}
                data['id'] = str(new.inserted_id)
                data['email'] = email
                data['name'] = name
                return return_success(data)
            else:
                return return_error(error="INVALID_VERIFY_KEY", message="Not valid verify key")

        else:
            return return_error(error="MISSING_FIELD", message="Field Missing")


@app.route("/email_verify", methods=["GET"])
def email_verify():
    args = request.args
    verify_code=args.get("code")
    verify_db = mongo_conn_obj.get_mongodb_connection().verify_link
    verify_data=verify_db.find_one({"code":verify_code})
    if verify_data:
        email=verify_data['email']
        type=verify_data['type']
        if type == 'register':
            redirect_url=APP_URL+"/signup?token="+verify_code+"&email="+email
        elif type == 'forgot_password':
            redirect_url=APP_URL+"/forgot-password?token="+verify_code+"&email="+email
        else:
            redirect_url=APP_URL+"/link-expired"
        return redirect(redirect_url)
    else:
        redirect_url=APP_URL+"/link-expired"
        return redirect(redirect_url)

@app.route('/login', methods=['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]

    users = mongo_conn_obj.get_mongodb_connection().user
    login_user = users.find_one({'email' : email})
    if login_user is None:
        return return_error("UNAUTHORIZED",code=401)
    if not bcrypt.check_password_hash(login_user['password'], password):
        return return_error("UNAUTHORIZED",code=401)

    session["email"] = email

    data={
        "id": str(login_user['_id']),
        "email": login_user['email']
    }
    return return_success(data=data,status="SUCCESS")


@app.route('/checksection')
def checksection():
    return jsonify({"section":session.get("email",None)})


@app.route("/logout")
@logged_in
def logout():
    try:
        del session["email"]
        return return_success(status="LOGOUT")
    except Exception as e:
        return return_error(message=str(e))

@app.route("/forgot_password", methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get("email", False)
    verify_key = data.get('verify_key', False)
    verify_db = mongo_conn_obj.get_mongodb_connection().verify_link
    user_db = mongo_conn_obj.get_mongodb_connection().user

    if not valid_email(email):
        return return_error(error="INVALID_EMAIL", message="invalid email")

    existing_user = user_db.find_one({'email': email})
    if not existing_user:
        return return_error(error="USER_NOT_FOUND", message="User not found")

    if email and not verify_key:
        # add entry in verify link table
        code = generate_random_string(12)
        new = verify_db.insert_one({'email': email, 'code': code, 'type': 'forgot_password'})
        # send verification link
        link = BACKEND_URL + "/email_verify?code=" + code
        sent = forgot_password_email(to_email=email, link=link)
        if sent:
            data = {
                "message": "verification mail is sent",
                "email": email
            }
            return return_success(data=data)
        else:
            return return_error()

    else:
        password = data.get("password", False)
        if email and verify_key and password:
            # check verify_key
            verify_data = verify_db.find_one({"email": email, "code": verify_key})
            if verify_data:
                # inset data
                hashpass = bcrypt.generate_password_hash(password)

                # Change password
                # new=user_db.insert_one({'email' : email, ,'name':name,"user_type":"INVESTOR",'setting':{'timezone':'Asia/Kolkata'}})
                filter = {}
                filter["email"] = email
                f_data = {
                    'password': hashpass
                }
                new_data = {"$set": f_data}
                x = user_db.update_one(filter, new_data)

                verify_db.delete_one({"email": email, "code": verify_key})
                session['email'] = email
                data = {}
                data['email'] = email
                return return_success(data)
            else:
                return return_error(error="INVALID_VERIFY_KEY", message="Not valid verify key")

        else:
            return return_error(error="MISSING_FIELD", message="Field Missing")
        # get verify key
        # get remaining registration info.


@app.route('/change_password', methods=['POST'])
@logged_in
def change_password():
    # get data from request
    data = request.get_json()
    email = data.get("email", False)
    password = data.get("password", False)
    old_password = data.get("old_password", False)

    if not email:
        return return_error(error="FIELD_MISSING", message="email field is missing")

    if not password:
        return return_error(error="FIELD_MISSING", message="password field is missing")

    if not old_password:
        return return_error(error="FIELD_MISSING", message="old password field is missing")

    user_db = mongo_conn_obj.get_mongodb_connection().user
    user_email = session.get("email", '')
    user = user_db.find_one({'email': user_email})

    if not bcrypt.check_password_hash(user['password'], old_password):
        return return_error("UNAUTHORIZED", code=401)

    if user and email == user_email:
        hashpass = bcrypt.generate_password_hash(password)

        filter = {}
        filter["email"] = email
        f_data = {
            'password': hashpass
        }
        new_data = {"$set": f_data}
        x = user_db.update_one(filter, new_data)
        if x:
            return return_success(data={'message': 'password updated successfully'})
    else:
        return return_error(message="user details not found")



def system_check():
    #check mongo connection
    print("Checking Mongo Connection")
    mongo_connection_check()

    #check redis connection
    print("Checking Redis Connection")
    redis_connection_check()
   

if __name__=="__main__":
    system_check()
    print('.....')
    print('FLASK_DEBUG',FLASK_DEBUG,type(FLASK_DEBUG))
    if FLASK_DEBUG == "True":
        app.run(debug=True,port=FLASK_PORT)
        app.config['DEBUG'] = True
    else:
        app.run(debug=False,port=FLASK_PORT)
        app.config['DEBUG'] = False
