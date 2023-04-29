from sqlalchemy import create_engine  
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String
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
	category = Column(String)
	profilePic = Column(String)
	
class Users(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	user = Column(String)
	password = Column(String)
	pathToProfilePicture = Column(String)

def Database(app):
	bcrypt = Bcrypt(app)
	engine = create_engine(f"postgresql://postgres:{PASSWORD_DB}@localhost/{NAME_DB}")
	Base.metadata.create_all(bind=engine)
	return engine