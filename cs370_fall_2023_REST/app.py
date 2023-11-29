from flask import Flask,render_template,request, redirect, url_for, g, session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.eeg import store_signup
import jwt
import gspread

import sys
import datetime
import bcrypt
import traceback

from tools.eeg import get_head_band_sensor_object


from db_con import get_db_instance, get_db

from tools.token_required import token_required

#used if you want to store your secrets in the aws valut
#from tools.get_aws_secrets import get_secrets

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"

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
@app.route('/',methods=['POST','GET']) #endpoint
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 
        return redirect(url_for('user', usr = username))
    else:
        return render_template("loginpage.html")



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 
        return redirect(url_for('user', usr = username))
    else:
        return render_template("loginpage.html")
        


@app.route('/index')
def loggeduser():
    if 'username' in session: #checks if a user is currently logged in
        username = session.get('username',None) #if no username exist then returns None instead
        print(f"Current user logged in is: {username}")
        return redirect('/static/index.html')  #grants access to video page
    else:
        return render_template("loginpage.html") #redirects to loginpage if no current user logged in
    
@app.route('<usr>')
def user(usr): 
    return redirect('login')


@app.route('/logout')
def logout():
    session.pop('username', None)  #session function that gets rid of the username stored on website, signing them out
    return render_template('loginpage.html') #redirects to the login page

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        rpassword = request.form.get('rpassword')

        print(username,password,rpassword)
        check = store_signup(username,password, rpassword)
        print(check)
        if check == True:
            session['username'] = username
            return redirect(url_for("user"))
        else:
            return render_template("accountregister.html")
    else:
        return render_template("accountregister.html")


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

