from flask import Blueprint
from flask import request, session, redirect

logout = Blueprint('logout', __name__)

@logout.route('/logout',methods = ['POST', 'GET'])
def logoutAuth():
    session["auth"] = None
    session["user"] = None
    return redirect('/') 