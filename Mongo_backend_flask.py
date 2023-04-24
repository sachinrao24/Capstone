from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('  ', 27017, username = " ", password = " ")  # first argument is the localhost name , second is mongodb localhost port number

db = client.flask_db  # flask_db is database name

@app.route("/")
def home_page():
    
    """
        Home page connection
    """

    return render_template(template_name_or_list)

@app.route("/")
def index() :
    
    """
        Index page navigation
    """
    
    return render_template(template_name_or_list)

@app.route("/home/exercises")
def exercises():

    """
        4 Different exercises page 
    """

    return render_template(template_name_or_list)

@app.route("/home/exercises/MediaPipeOutput")
def cam_instance():

    """
        Mediapipe camera instance 
    """

    return render_template(template_name_or_list)


if __name__ =='__main__':
    app.run(debug=True)

