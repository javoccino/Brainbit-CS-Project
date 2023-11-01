from flask import Blueprint, render_template, request,flash

auth = Blueprint('auth', __name__)
testing = 'here'


@auth.route('/login',methods=['POST','GET'])
def login():
    #data = request.form
    #print(data)
    return render_template("loginpage.html")

@auth.route('/logout')
def logout():
    return render_template()

@auth.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        rpassword = request.form.get('rpassword')
    
        if password != rpassword:
            flash('Wrong password', category='error')
        else:
            flash('Account has been created!', category='success')
    return render_template("accountregister.html")

