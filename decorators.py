from flask import g,redirect,url_for
from functools import wraps

def login_required(func):
    @wraps(func)
    def inner(*arg,**kwargs):
        if hasattr(g,"user"):
            func(*arg,**kwargs)
        else:
            return redirect(url_for("user.login"))
    return inner