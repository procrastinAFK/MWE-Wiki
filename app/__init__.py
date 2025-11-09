# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from data import *

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

    if request.method == 'POST':
        try:
            if auth(request.form['username'], request.form['password']):
                session['username'] = request.form['username']
                return redirect("/home")

        except ValueError as e:
                return render_template('login.html', error=e)

    return render_template('login.html');


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            register_user(request.form['username'], request.form['password'])
            session['username'] = request.form['username']
            return redirect("/home")

        except ValueError as e:
            return render_template('register.html', error=e)

    return render_template('register.html')


@app.route("/home", methods=['GET','POST'])
def home():
    if not 'username' in session:
        return redirect("/")

    if 'logout' in request.form:
        session.clear()
        return redirect('/')

    username = session['username']

    if 'profile' in request.form:
        return render_template('profile.html', username=username, blogs=get_blogs(username))

    blog_keys = all_blogs()

    for ID in blog_keys:
        if f'{ID}' in request.form:
            return render_template('viewblog.html', blogid=ID)

    blog_info = [[blog_keys[i], get_blog_name(blog_keys[i]), get_blog_author(blog_keys[i])] for i in range(len(blog_keys))]

    return render_template('home.html', username=username, blogs=blog_info)


@app.route("/editpf", methods=['GET', 'POST'])
def editpf():
    if not 'username' in session:
        return redirect("/")

    if request.method == 'POST':
        if 'username_form' in request.form:
            try:
                print("form" + request.form['username'])
                change_username(session['username'], request.form['username'])
                session.clear()
                session['username'] = request.form['username']

            except ValueError as e:
                return render_template('editpf.html', username=session['username'], bio=get_bio(session['username']), error=e)

        if 'password_form' in request.form:
            try:
                change_password(session['username'], request.form['old_pass'], request.form['new_pass'])

            except ValueError as e:
                return render_template('editpf.html', username=session['username'], bio=get_bio(session['username']), error=e)

        if 'bio_form' in request.form:
            change_bio(session['username'], request.form['bio'])

        if 'logout' in request.form:
            session.clear()
            return redirect('/')

    return render_template('editpf.html', username=session['username'], bio=get_bio(session['username']))


@app.route("/viewblog", methods=['GET', 'POST'])
def viewblog():
    if not 'username' in session:
        return redirect("/")

    entries = get_entries(blogid)

    if request.method == 'POST':
        for entryid in entries:
            if f'{entryid}' in request.form:
                return redirect(url_for('editntry', entryid=f'{entryid}'))

        if 'logout' in request.form:
            session.clear()
            return redirect('/')

    return render_template('viewblog.html', blogid=blogid)


@app.route("/viewblog", methods=['GET', 'POST'])
def viewblog():
    username = session["username"]
    return render_template("viewblog.html", username = username)

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    username = session["username"]
    return render_template("profile.html", username = username)


if (__name__ == "__main__"):
    app.debug = True; # temporary!
    app.run()
