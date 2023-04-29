from flask import Flask, jsonify
from flask import render_template
from flask import request, session
from sqlalchemy.orm import Session
from DB import Database, Text, Users
from func import download_file
from flask import Blueprint
from utils import return_posts_by_category_json_all

app = Flask(__name__)
engine = Database(app)

api = Blueprint('api', __name__)

#Handler on nonexist post
@api.route('/api/posts', methods=['GET', 'POST'])  
def ret_posts():
	
	

    return jsonify(return_posts_by_category_json_all())

@api.route('/api/posts/<id>', methods=['GET', 'POST'])  
def ret_post():
	pass    

@api.route('/api/posts/random', methods=['GET', 'POST'])  
def ret_post_random():
    pass