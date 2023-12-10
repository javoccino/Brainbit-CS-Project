from flask import Flask,render_template,request, redirect, url_for, g, session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.eeg import store_signup,  returnpswrd ,checkUser
from tools.compare import compare_data
import jwt

import sys
import datetime
import bcrypt
import traceback

import requests
import os

from tools.eeg import get_head_band_sensor_object


from db_con import get_db_instance, get_db

from tools.token_required import token_required

#used if you want to store your secrets in the aws valut
#from tools.get_aws_secrets import get_secrets

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"

API_KEY = os.getenv('googlesheetsapikey') #grabbing the api key from my local machine
sheet_id = "1a3e1r-aGk1SbDKgs3wYYR_Mjc3OQ-hkEVl47Ll3uqIg" #id of the sheet grabbed from url to create url api call
range = 'Responses!A1:D100' #sheetname following by ranges to be displayed

#creating the url with sheet_id, range, and apikey to access the sheet that holds all the survey data to be called using request
url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range}?key={API_KEY}'

#Create our app
app = Flask(__name__)
#add in flask json
FlaskJSON(app)
app.secret_key="secretkey"

#g is flask for a global var storage 
def init_new_env():
    #To connect to DB
    if 'db' not in g:
        g.db = get_db()

    if 'hb' not in g:
        g.hb = get_head_band_sensor_object()

    #g.secrets = get_secrets()
    #g.sms_client = get_sms_client()

#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
#@app.route('/') #endpoint
#def index():
    #return redirect('/static/index.html')

#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
@app.route('/',methods=['POST','GET']) #endpoint
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        if(checkUser(username)==False):
            return render_template("loginpage.html")
        password = request.form.get('password')
        if password == returnpswrd(username):
            session['username'] = username
            return redirect("/loggedin")
        else:
            return render_template("loginpage.html")
    return render_template("loginpage.html")

#@app.route('/<usr>')
#def user(usr):
 #   return redirect('/login')


@app.route('/loggedin',methods=['POST','GET'])
def loggedin():
    if 'username' in session:
        username = session.get('username', None)
        print(f"Current user logged in is: {username}")

        return  redirect("static/index.html")

@app.route('/logout')
def logout():
    user = session.get('username', None)
    print(f"{user} has logged out")
    session.pop('username', None)  #session function that gets rid of the username stored on website, signing them out
    #return render_template('loginpage.html') #redirects to the login page
    return redirect(url_for('index'))

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        rpassword = request.form.get('rpassword')
        email = request.form.get('email')

        print(username,password,rpassword,email)
        check = store_signup(username,password, rpassword,email)
        print(check)
        if check == True:
            session['username'] = username
            return redirect(url_for("loggedin"))
        else:
            return render_template("accountregister.html")
    else:
        return render_template("accountregister.html")

@app.route('/matchpage')
def matchpage():
    if 'username' in session:
        print(session['username'])

        username = session['username']
    
        response = requests.get(url) #stores the Response information from the get request into response
        print(response)
        if response.status_code == 200: #.status_code grabs response code, 200 means success
            data = response.json() #storing json content into data as a dictionary
            print(data)
            vals = data.get('values', [])  #storing the values field from the json repsonse into a list called vals
            
        else:
            print("fail")
        


        list = compare_data(username, vals)
        #print(list)
        print(len(list))

        #for item in matching_list:
         #   print(item)
            

            
        
        return render_template('matchpage.html',username = username, len = len(list), list = list, count = 0)

@app.route("/secure_api/<proc_name>",methods=['GET', 'POST'])
@token_required
def exec_secure_proc(proc_name):
    logger.debug(f"Secure Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('secure_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp



@app.route("/open_api/<proc_name>",methods=['GET', 'POST'])
def exec_proc(proc_name):
    logger.debug(f"Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('open_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

