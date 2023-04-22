import os
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
profile = Blueprint('profile', __name__)

print()

@profile.route('/profile',methods = ['POST', 'GET'])
def profileFunc():
    user = session["user"]
    userImage = ""
    dataFile = None
    
    with Session(autoflush=False, bind=engine) as db:
        try:
            userDB = db.query(Users).filter(Users.user==user).one_or_none()
            print(f"{userDB.id}.{userDB.user}.{userDB.pathToProfilePicture}")
            userImage = userDB.pathToProfilePicture
            print(userImage)
        except AttributeError:
            print("User not finded")
    if request.method == 'POST':
        dataFile = download_file(request)
        print("данные картинки в профиле", dataFile)
        with Session(autoflush=False, bind=engine) as db:
            
                userDB = db.query(Users).filter(Users.user==user).one_or_none()
                userDB.pathToProfilePicture = dataFile["filename"]
              
                db.commit()
    if userImage != "":
        return render_template('profile.html', name=user, image=userImage)
    else:
        return render_template('profile.html', name=user)