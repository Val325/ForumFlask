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
import datetime
import requests
import os

app = Flask(__name__)
UPLOADS_PATH = 'static'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.secret_key = '16a2df16fa546ae0a121f99f59390b89f05782905e966299559be0454fbf9856f9ecece36006dd0dcb26dee5e9a6deab2716c98976027579578617d3b00771f6'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_file(request):
    filename = ''
    image_src = ''
    file = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_src = app.config['UPLOAD_FOLDER'] + filename

        
        
        full_filename = os.path.join(os.path.join('uploads'), filename)

        filedata = {
            "filename": filename,
            "full_filename": full_filename,
            "source": image_src, 
            "file": file
        }
        return filedata

bcrypt = Bcrypt(app)
engine = create_engine("postgresql://postgres:Hamachi2002@localhost/flaskDB")

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

Base.metadata.create_all(bind=engine)

@app.route('/',methods = ['POST', 'GET'])
def index():
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

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_src = app.config['UPLOAD_FOLDER'] + filename

        print("Path:", image_src)
        print('filename', filename)
        full_filename = os.path.join(os.path.join('uploads'), filename)

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
                            nameImage=filename, 
                            pathPost=postPath,
                            profilePic=profilePic)
                db.add(post)     
                db.commit()     
                
            return redirect("/")
            #return render_template('index.html', posts=posts)
        else:

            return render_template('index.html', posts=posts,
                session=IsAuth, 
                nameUser=User)
            

@app.route('/registration',methods = ['POST', 'GET'])
def registration():
    userImage = ""
    if request.method == 'POST':
        print("registration route here post")

        print("User:", request.form.get('Username',''))
        user = request.form.get('Username','')

        print("Password: ", request.form.get('Password',''))
        password = request.form.get('Password','')

        hashed = bcrypt.generate_password_hash(password).decode('utf-8') 
        print("Hashed password:", hashed)

        with Session(autoflush=False, bind=engine) as db:
            User = Users(user=user, password=hashed, pathToProfilePicture=userImage)
            db.add(User)
            db.commit()
            return redirect("/")

    return render_template('registration.html')
    

@app.route('/login',methods = ['POST', 'GET'])
def login():
    passDB = ''
    if request.method == 'POST':
        print("login route here post")

        print("User:", request.form.get('Username',''))
        user = request.form.get('Username','')

        print("Password: ", request.form.get('Password',''))
        password = request.form.get('Password','')

        with Session(autoflush=False, bind=engine) as db:
            try:
                userDB = db.query(Users).filter(Users.user==user).one_or_none()
                print(f"{userDB.id}.{userDB.user} ({userDB.password})")

                IsAuthBool = bcrypt.check_password_hash(userDB.password, password)
                print("Is password correct?", IsAuthBool)
                session["auth"] = IsAuthBool
                session["user"] = userDB.user  
                return redirect("/")
            except AttributeError:
                print("User not finded")
            
        


    return render_template('login.html')

@app.route('/logout',methods = ['POST', 'GET'])
def logout():
    session["auth"] = None
    session["user"] = None
    return redirect('/') 

@app.route('/post/<id>', methods=['GET', 'POST'])  
def post(id):
    IsAuth = session["auth"]
    User = session["user"]

    idUser = ''
    DbUser = ''
    DbPost = ''
    DbPathImage = '/post/' + str(id)
    DbNameImage = ''
    dataFile = download_file(request)
    posts = []
    userImage = ""
    
    
    with Session(autoflush=False, bind=engine) as dbOut:
        post = dbOut.get(Text, id)
        posts = dbOut.query(Text).filter(Text.pathPost==DbPathImage)
        user = dbOut.query(Users).filter(Users.user==User).one_or_none()
        for p in posts:
            print(f"Подпосты - id:{p.id};user:{p.name};post:{p.text};image:{p.nameImage}")

        print(f"id:{post.id};user:{post.name};post:{post.text};image:{post.nameImage}")
        print(f"User - id:{user.id};user:{user.user};pictueProfile:{user.pathToProfilePicture}")
        
        userImage = user.pathToProfilePicture
        idUser = post.id
        DbUser = post.name
        DbPost = post.text
        DbNameImage = post.nameImage

        print("Id User:", idUser)
        print("DB User:", DbUser)
        print("DB Post", DbPost)
        print("DB Path Image", DbPathImage)
        print("DbNameImage", DbNameImage)


        if request.method == 'POST':
            result = request.form
            with Session(autoflush=False, bind=engine) as db:
                result = request.form
                
                Post = Text(name=DbUser,
                    text=result.get('post',''), 
                    nameImage=dataFile["filename"], 
                    pathPost=DbPathImage,
                    profilePic=userImage)
                db.add(Post)     
                db.commit()


    return render_template('subposts.html',
        id=idUser,
        text=DbPost,
        session=IsAuth, 
        nameUser=post.name,
        nameImage=DbNameImage,
        posts=posts,
        image=userImage)
#
@app.route('/profile',methods = ['POST', 'GET'])
def profile():
    user = session["user"]
    userImage = ""
    dataFile = None
    
    with Session(autoflush=False, bind=engine) as db:
        try:
            userDB = db.query(Users).filter(Users.user==user).one_or_none()
            print(f"{userDB.id}.{userDB.user}")
            userImage = userDB.pathToProfilePicture
        except AttributeError:
            print("User not finded")
    if request.method == 'POST':
        dataFile = download_file(request)
        print("данные картинки в профиле", dataFile)
        with Session(autoflush=False, bind=engine) as db:
            
                userDB = db.query(Users).filter(Users.user==user).one_or_none()
                userDB.pathToProfilePicture = dataFile["filename"]
              
                db.commit()
    if dataFile:
        return render_template('profile.html', name=user, image=userImage)
    else:
        return render_template('profile.html', name=user) 

@app.route('/weather',methods = ['POST', 'GET'])
def weatherAPI():
    dataWeather = requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Zaporozhye?unitGroup=metric&key=G8GP3VDB66XR9WCHZ64UCRVNP&contentType=json')
    today = datetime.datetime.today()

    print( today.strftime("%Y-%m-%d") ) # %Y-%m-%d
    todayTime = today.strftime("%Y-%m-%d")

    print(f'сегодня {todayTime} температура в Запорожье: ',dataWeather.json()['days'][0]['temp'])
    tomorrow = today + datetime.timedelta(days=1)

    print(f'завтра {tomorrow.date()} температура в Запорожье: ',dataWeather.json()['days'][1]['temp'])
    return render_template('weather.html', todayTime=today.strftime("%Y-%m-%d"), forecastToday=dataWeather.json()['days'][0]['temp'], forecastTomorrow=dataWeather.json()['days'][1]['temp'])