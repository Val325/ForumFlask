from flask import Flask, redirect, current_app
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
import datetime
import requests
import os
import getApiWeather
import profile
import logout
import login
import registration
import posts
import subposts
import category
from DB import Database, Text, Users
from func import allowed_file, download_file

app = Flask(__name__)
engine = Database(app)

def return_posts_by_category(category):
	with Session(autoflush=False, bind=engine) as db:
    	# получение всех объектов
		user_posts = db.query(Text).filter(Text.category == category)
	return user_posts

def post_category(category,
					name,
					text,
					nameImage,
					pathPost,
					profilePic):

	with Session(autoflush=False, bind=engine) as db:
		"""
		result = request.form
                
		Post = Text(name=DbUser,
					text=result.get('post',''), 
					nameImage=dataFile["filename"], 
					pathPost=DbPathImage,
					profilePic=userImage)

		result = request.form
        """
		Post = Text(name=name,
					text=text, 
					nameImage=nameImage, 
					pathPost=pathPost,
					profilePic=profilePic,
					category=category)
		b.add(Post)     
		db.commit()

def ret_profile_picture(user):
	with Session(autoflush=False, bind=engine) as db:
		userDB = db.query(Users).filter(Users.user==user).one_or_none()
		try:
			profilePic = userDB.pathToProfilePicture
		except AttributeError:
			profilePic = ""

	return profilePic
