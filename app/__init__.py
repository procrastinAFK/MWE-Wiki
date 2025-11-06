# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from flask import Flask, render_template, request, session, redirect
import sqlite3
from data import *


app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'asdhajskjbweifnoihgis'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(auth(request.form['username'], request.form['password']))
        if auth(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect("/home")

    elif 'username' in session:
        return redirect("/home")

    return render_template('login.html');


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_user(request.form['username'], request.form['password'])
        return redirect("/")
    else:
        return render_template('register.html')


@app.route("/home", methods=['GET','POST'])
def home():
    if 'logout' in request.form:
        session.clear()
        return redirect('/')

    username = session['username']

    blog_keys = all_blogs()
    blog_info = [[get_blog_name(all_blogs[i]), get_blog_author(all_blogs[i])] for i in range(len(blog_keys))]

    return render_template('home.html', username, blogs=blog_info)


if (__name__ == "__main__"):
    app.debug = True; # temporary!
    app.run()
