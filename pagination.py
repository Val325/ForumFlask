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
from DB import Database, Text, Users
from func import allowed_file, download_file

app = Flask(__name__)
engine = Database(app)
current_page = 1
max_page_per = 5

def amountItemsInDB():
	amount = 0
	with Session(autoflush=False, bind=engine) as db:
    	# получение всех объектов
		user_posts = db.query(Text).all()
		print("---------")
		for p in user_posts:
			print(f"id:{p.id};user:{p.name};post:{p.text};image:{p.nameImage}")
			amount = amount + 1
		print("---------")
		print("часть")
		print("---------")
		for p in user_posts[2:4]:
			print(f"id:{p.id};user:{p.name};post:{p.text};image:{p.nameImage}")
			#amount = amount + 1
		print("---------")
		print("amount posts")
		print(amount)
	return amount

def amountItemsInDB_S(category):
	amount = 0
	with Session(autoflush=False, bind=engine) as db:
    	# получение всех объектов
		user_posts = db.query(Text).filter(Text.category == category)
		print("---------")
		for p in user_posts:
			print(f"id:{p.id};user:{p.name};post:{p.text};image:{p.nameImage}")
			amount = amount + 1
		
		print(amount)
	return amount

def get_DB(offset=0, per_page=5):
	amount = 0
	with Session(autoflush=False, bind=engine) as db:
    	# получение всех объектов
		user_posts = db.query(Text).all()
		print("---------")
		for p in user_posts:
			print(f"id:{p.id};user:{p.name};post:{p.text};image:{p.nameImage}")
			amount = amount + 1
		print("---------")
		print("часть")
		print("---------")
		for p in user_posts[2:4]:
			print(f"id:{p.id};user:{p.name};post:{p.text};image:{p.nameImage}")
			#amount = amount + 1
		print("---------")
		print("amount posts")
		print(amount)
		return user_posts[offset:offset + per_page]

def get_current_page():
	return current_page

def get_next_page():
	return current_page + 1

def get_previous_page():
	return current_page - 1

def get_max_page():
	return max_page_per

def amount_articles_per_page(amount):
	return round(amount / max_page_per)

def get_array_number_page(amount):
	array = [0]
	# + 1 is offset
	for n in range(1, amount):
		array.append(n)

	return array