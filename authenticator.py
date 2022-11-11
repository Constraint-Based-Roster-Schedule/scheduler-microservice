from functools import wraps

import jwt 
from flask import redirect, request, url_for

import config


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try :
            token = request.headers['access-token']
            data = jwt.decode(token, key=config.SECRET_KEY, algorithms=['HS256'])
            print (data['message'])
        except :
            return redirect(url_for("accessError"))
        
        print("logged in")
        return f(*args, **kwargs)
    return decorated_function

