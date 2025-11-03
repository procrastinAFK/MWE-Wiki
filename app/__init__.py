# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from flask import Flask, render_template, request, session, redirect
import sqlite3
import subprocess
from data import *

subprocess.run(["python", "data.py"])

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'asdhajskjbweifnoihgis'

@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect("/home")
    
    print("idk even more")
    if request.method == 'POST':
        print("maybe good things")
        if auth(request.form['username'], request.form['password']):
            print("good things")
            session['username'] = request.form['username']
            return redirect("/home")
    else:
        return render_template('login.html');

@app.route("/home", methods=['GET','POST']) # will need to use post for password at the very least
def authenticate():
    return render_template('home.html') 

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_user(request.form['username'], request.form['password'])
        return redirect("/")
    else:
        return render_template('register.html')

if (__name__ == "__main__"):
    app.debug = True; # temporary!
    app.run()