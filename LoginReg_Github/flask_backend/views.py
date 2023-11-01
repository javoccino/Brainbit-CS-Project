from flask import Blueprint, render_template
#help us split up and organize

views = Blueprint('views', __name__)

#endroute?
@views.route('/')
def home():
    return render_template("home.html")


