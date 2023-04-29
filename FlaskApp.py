from flask import Flask
import getApiWeather
import profile
import logout
import login
import registration
import posts
import subposts
import category
import errors
import api
from DB import Database


app = Flask(__name__)

UPLOADS_PATH = 'static'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.secret_key = '16a2df16fa546ae0a121f99f59390b89f05782905e966299559be0454fbf9856f9ecece36006dd0dcb26dee5e9a6deab2716c98976027579578617d3b00771f6'
engine = Database(app)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.register_blueprint(getApiWeather.weatherAPI)
app.register_blueprint(profile.profile)
app.register_blueprint(logout.logout)
app.register_blueprint(login.login)
app.register_blueprint(posts.posts)
app.register_blueprint(subposts.subposts)
app.register_blueprint(registration.registrationUser)
app.register_blueprint(category.cat)
app.register_blueprint(errors.errorHandler)    
app.register_blueprint(api.api) 
