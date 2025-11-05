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
    if request.method == 'POST':
        #print("maybe good things")
        print(auth(request.form['username'], request.form['password']))
        if auth(request.form['username'], request.form['password']):
            #print("good things")
            session['username'] = request.form['username']
            return redirect("/home")

    elif 'username' in session:
        return redirect("/home")

    return render_template('login.html');

@app.route("/home", methods=['GET','POST']) # will need to use post for password at the very least
def home():
    return render_template('home.html', username = session['username'])

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
