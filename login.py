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
login = Blueprint('login', __name__)
bcrypt = Bcrypt(app)

@login.route('/login',methods = ['POST', 'GET'])
def loginAuth():
    passDB = ''
    if request.method == 'POST':
        print("login route here post")

        print("User:", request.form.get('Username',''))
        user = request.form.get('Username','')

        print("Password: ", request.form.get('Password',''))
        password = request.form.get('Password','')

        with Session(autoflush=False, bind=engine) as db:
            try:
                userDB = db.query(Users).filter(Users.user==user).one_or_none()
                print(f"{userDB.id}.{userDB.user} ({userDB.password})")

                IsAuthBool = bcrypt.check_password_hash(userDB.password, password)
                print("Is password correct?", IsAuthBool)
                session["auth"] = IsAuthBool
                session["user"] = userDB.user  
                return redirect("/")
            except AttributeError:
                print("User not finded")
            
        


    return render_template('login.html')