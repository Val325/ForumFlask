from flask import Blueprint, Flask
from flask import request, session, redirect
from flask import render_template, current_app
from func import allowed_file, download_file
from utils import return_posts_by_category, ret_profile_picture
from DB import Database, Text, Users
from pagination import amountItemsInDB_S, get_current_page, get_max_page, get_DB, max_page_per, amountItemsInDB
from pagination import get_next_page, get_previous_page, amount_articles_per_page, get_array_number_page

app = Flask(__name__)
cat = Blueprint('category', __name__)
engine = Database(app)


@cat.route('/category',methods = [ 'GET'])
def category():
	IsAuth = session["auth"]
	print("session:", IsAuth)
	User = session["user"]
	print("user:", User)


	return render_template('categoryChoice.html',
				session=IsAuth, 
                nameUser=User)	

@cat.route('/category/<category>/<page>',methods = ['POST', 'GET'])
def index(category,page):
	IsAuth = session["auth"]
	print("session:", IsAuth)
	User = session["user"]
	print("user:", User)


	idUser = ''
	DbUser = ''
	DbPost = ''
	DbPathImage = '/post/' + str(id)
	DbNameImage = ''
	dataFile = download_file(request)
	posts = []
	userImage = ""

	posts = return_posts_by_category(category)
	articles_per_page_arr = get_array_number_page(amount_articles_per_page(amountItemsInDB_S(category)))
	picture = ret_profile_picture(User)

	if request.method == 'POST':
		pass

	
	return render_template('category.html',
				category=category,
				posts=posts[0 + 5 * int(page):5 + 5 * int(page)],
				session=IsAuth, 
                nameUser=User,
                image=picture,
                pages=articles_per_page_arr)	