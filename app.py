from flask import Flask, render_template, request 
from authenticator import token_required
from scheduler import runScheduler 

app = Flask(__name__)
app.config.from_pyfile("config.py") 

@app.route('/')
def index():
    return "hello world"


@app.route('/schedule')
@token_required
def schedule():
    outvalue = runScheduler()
    return outvalue

@app.route('/error') 
def accessError() : 
    return {"message" : "token invalid" }, 403




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 