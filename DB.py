from flask import Blueprint
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
from config import PASSWORD_DB, NAME_DB



class Base(DeclarativeBase): pass

class Text(Base):
	__tablename__ = "posts"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	text = Column(String)
	nameImage = Column(String)
	pathPost = Column(String) # URL for post
	profilePic = Column(String)
	
class Users(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	user = Column(String)
	password = Column(String)
	pathToProfilePicture = Column(String)

def Database(app):
	bcrypt = Bcrypt(app)
	engine = create_engine("postgresql://postgres:Hamachi2002@localhost/flaskDB")
	Base.metadata.create_all(bind=engine)
	return engine