from flask import Flask, redirect
from flask import render_template
from flask import request, session
from os.path import join
from werkzeug.utils import secure_filename
from sqlalchemy.orm import Session
import os
from DB import Database, Text, Users
from func import allowed_file, download_file
from flask import Blueprint
from config import UPLOADS_PATH, ALLOWED_EXTENSIONS
from pagination import amountItemsInDB, get_current_page
from pagination import amount_articles_per_page, get_array_number_page


app = Flask(__name__)
engine = Database(app)
#with app.app_context():

posts = Blueprint('post', __name__)
print("engine:", engine)
print("array", get_array_number_page(amountItemsInDB()))
print("current_amount_pages",get_current_page())
print("current_page",get_current_page())
print("amount_articles_per_page", amount_articles_per_page(amountItemsInDB()))
print("array_amount_articles_per_page", get_array_number_page(amount_articles_per_page(amountItemsInDB())))
articles_per_page_arr = get_array_number_page(amount_articles_per_page(amountItemsInDB()))



@posts.route('/')
def redir():
    return redirect("/category")

@posts.route('/<page>',methods = ['POST', 'GET'])
def index(page):
    try:
        IsAuth = session["auth"]
        User = session["user"]
    
        image_src = ''
        filename = ''
        
        profilePic = ""
        print("auth:",session["auth"])
        print("username:",session["user"])
    except KeyError:
        IsAuth = False
        User = "anon"
    postPath = "/"

    #--------------#
    # Upload image #
    #--------------#

    dataFile = download_file(request)

    #--------------#
    # Upload image #
    #--------------#

    with Session(autoflush=False, bind=engine) as db:
        posts = db.query(Text).filter(Text.pathPost==postPath)
        userDB = db.query(Users).filter(Users.user==User).one_or_none()

        try:
            profilePic = userDB.pathToProfilePicture
        

            for p in posts:
                print(f"id:{p.id};user:{p.name};post:{p.text};image:{p.nameImage}")

        
            print(f"id:{userDB.id};user:{userDB.user};post:{userDB.pathToProfilePicture}")

        except AttributeError:
            profilePic = ""

        if request.method == 'POST':
            result = request.form
            print(result)
            print(result.get('post',''))
            
            with Session(autoflush=False, bind=engine) as db:
                post = Text(name=User,
                            text=result.get('post',''), 
                            nameImage=dataFile["filename"], 
                            pathPost=postPath,
                            profilePic=profilePic,
                            category=result.get('select_cat',''))
                db.add(post)     
                db.commit()     
                
            return redirect("/0")
            #return render_template('index.html', posts=posts)
        else:
            # от 0 до 5, а при каждом щелчке page + 5
            # первый 0:5 [0 + 5 * page:5 + 5 * page]; page = 1 
            # второй 5:10
            return render_template('index.html', posts=posts[0 + 5 * int(page):5 + 5 * int(page)],
                session=IsAuth, 
                nameUser=User,
                image=profilePic,
                pages=articles_per_page_arr)	