from flask import Flask
from flask import render_template
from flask import request, session
from sqlalchemy.orm import Session
from DB import Database, Text, Users
from func import download_file
from flask import Blueprint

app = Flask(__name__)
engine = Database(app)

subposts = Blueprint('subposts', __name__)
print("engine:",engine)

@subposts.route('/post/<id>', methods=['GET', 'POST'])  
def post(id):
    try:
        IsAuth = session["auth"]
        User = session["user"]
    except KeyError:
        print('not error')
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
        
        user = dbOut.query(Users).filter(Users.id==id).one_or_none()
        for p in posts:
            print(f"Подпосты - id:{p.id};user:{p.name};post:{p.text};image:{p.nameImage}")

        
        
        print(f"id:{post.id};user:{post.name};post:{post.text};image:{post.nameImage}")
        #print(f"User - id:{user.id};user:{user.user};pictueProfile:{user.pathToProfilePicture}")
        userImage = post.profilePic

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

    try:
        return render_template('subposts.html',
            id=idUser,
            text=DbPost,
            session=IsAuth, 
            nameUser=post.name,
            nameImage=DbNameImage,
            posts=posts,
            image=userImage)
    except UnboundLocalError:
        return render_template('subposts.html',
            id=idUser,
            text=DbPost, 
            nameUser=post.name,
            nameImage=DbNameImage,
            posts=posts,
            image=userImage)