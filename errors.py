from flask import Flask
from flask import render_template
from flask import request, session
from sqlalchemy.orm import Session
from DB import Database, Text, Users
from func import download_file
from flask import Blueprint
from utils import return_posts_by_category_array

app = Flask(__name__)
engine = Database(app)

errorHandler = Blueprint('errorHandler', __name__)

#Handler on nonexist post
@errorHandler.route('/post/<id>', methods=['GET', 'POST'])  
def post(id):
    category1 = return_posts_by_category_array('category1')
    category2 = return_posts_by_category_array('category2')
    category3 = return_posts_by_category_array('category3')
    amount = category1 + category2 + category3

    if id not in amount:
        abort(404)

    return redirect(f"/post/{id}")