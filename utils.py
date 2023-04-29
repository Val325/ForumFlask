from flask import Flask
from flask import request
from sqlalchemy.orm import Session
import category
from DB import Database, Text, Users

app = Flask(__name__)
engine = Database(app)

def return_posts_by_category_json_all():
	json = {}
	with Session(autoflush=False, bind=engine) as db:
    	# получение всех объектов
		user_posts = db.query(Text).all()
		for post in user_posts:
			json.update({
				str(post.id):{
				"id":post.id,
				"name":post.name,
				"text":post.text,
				"category":post.category,
				},
				str(post.name):{
				"id":post.id,
				"name":post.name,
				"text":post.text,
				"category":post.category,
				}
			}) 

	return json


def return_all_posts_amount():
	amount_posts = 0
	with Session(autoflush=False, bind=engine) as db:
		user_posts = db.query(Text).all()
		for post in user_posts:
			amount_posts = amount_posts + 1

	return amount_posts

def return_posts_by_category_array(category):
	posts = []
	with Session(autoflush=False, bind=engine) as db:
    	# получение всех объектов
		user_posts = db.query(Text).filter(Text.category == category)
		for post in user_posts:
			posts.append(post.id)
	return posts

def return_posts_by_category_amount(category):
	amount_posts = 0
	with Session(autoflush=False, bind=engine) as db:
    	# получение всех объектов
		user_posts = db.query(Text).filter(Text.category == category)
		for post in user_posts:
			amount_posts = amount_posts + 1
	return amount_posts

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


def send_category_post(request, name, text, nameImage, pathPost, profilePic, category):

	with Session(autoflush=False, bind=engine) as db:
			
			
			Post = Text(name=name,
						text=text, 
						nameImage=nameImage, 
						pathPost=pathPost,
						profilePic=profilePic,
						category=str(category))
			db.add(Post)     
			db.commit()