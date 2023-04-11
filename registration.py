import datetime
import requests
import os
import getApiWeather
import profile
import logout
from flask import Flask, redirect
from flask import render_template
from flask import request, session
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine  
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import  Column, Integer, String
from sqlalchemy import select
from flask_bcrypt import Bcrypt
from DB import Database, Text, Users
from func import allowed_file, download_file
from flask import Blueprint

app = Flask(__name__)
engine = Database(app)
registrationUser = Blueprint('registration', __name__)
bcrypt = Bcrypt(app)

@registrationUser.route('/registration',methods = ['POST', 'GET'])
def registration():
    userImage = ""
    if request.method == 'POST':
        print("registration route here post")

        print("User:", request.form.get('Username',''))
        user = request.form.get('Username','')

        print("Password: ", request.form.get('Password',''))
        password = request.form.get('Password','')

        hashed = bcrypt.generate_password_hash(password).decode('utf-8') 
        print("Hashed password:", hashed)

        with Session(autoflush=False, bind=engine) as db:
            User = Users(user=user, password=hashed, pathToProfilePicture=userImage)
            db.add(User)
            db.commit()
            return redirect("/")

    return render_template('registration.html')