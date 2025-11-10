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
    style = url_for('static', filename='style.css')
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
                return render_template('login.html', url=style, error=e)



    return render_template('login.html', url=style);


@app.route("/register", methods=['GET', 'POST'])
def register():
    style = url_for('static', filename='style.css')
    if request.method == 'POST':
        try:
            register_user(request.form['username'], request.form['password'])
            session['username'] = request.form['username']
            return redirect("/home")

        except ValueError as e:
            return render_template('register.html', url=style, error=e)

    return render_template('register.html', url=style)


@app.route("/home", methods=['GET','POST'])
def home():
    style = url_for('static', filename='style.css')
    if not 'username' in session:
        return redirect("/")

    if 'logout' in request.form:
        session.clear()
        return redirect('/')

    username = session['username']

    if 'profile' in request.form:
        return render_template('profile.html', username=username, blogs=get_blogs(username), url=style)

    blog_keys = all_blogs()
    if blog_keys[0] == 'None':
        blog_keys = blog_keys[1:]

    for ID in blog_keys:
        if f'{ID}' in request.form:
            session['blogid'] = f'{ID}'
            return redirect('/viewblog', url=style)

    blog_info = [[blog_keys[i], get_blog_name(blog_keys[i]), get_blog_author(blog_keys[i])] for i in range(len(blog_keys))]

    return render_template('home.html', username=username, blogs=blog_info, url=style)


@app.route("/viewblog", methods=['GET', 'POST'])
def viewblog():
    
    if not 'username' in session:
        return redirect("/")

    username = session["username"]
    blogid = session['blogid']
    blogname = get_blog_name(blogid)
    author_username = get_blog_author(blogid)
    entries = get_entries(blogid)

    if request.method == 'POST':
        for entryid in entries:
            if f'{entryid}' in request.form:
                return redirect(url_for('editntry', entryid=f'{entryid}'))

    if 'logout' in request.form:
        session.clear()
        return redirect('/')
    
    data = [[entries[i], get_entry_name(entries[i]), get_entry_author(entries[i]), get_entry_contents(entries[i])] for i in range(len(entries))]
    return render_template('viewblog.html', username=username, author=author_username, name=blogname, blogid=blogid, entries=data)


@app.route("/newblog", methods=['GET', 'POST'])
def newblog():

    if not 'username' in session:
        return redirect("/")

    if 'logout' in request.form:
        session.clear()
        return redirect('/')

    username = session["username"]

    return render_template('newblog.html', username=username)


# helper for new_blog
@app.route("/create", methods=['GET', 'POST'])
def create_blog():

    if not 'username' in session:
        return redirect("/")

    username = session["username"]
    blogid = add_blog(request.form['newblog_title'], username)
    session['blogid'] = f'{blogid}'
    return redirect('/viewblog')


# helper for editntry
@app.route("/new_entry", methods=['GET', 'POST'])
def new_entry():
    
    if not 'username' in session:
        return redirect("/")
    
    username = session["username"]
    blogid = session['blogid']
    entry_id = add_entry(request.form['new_entry'], '')
    session['entryid'] = f'{entryid}'
    return redirect('/editntry')


@app.route("/profile", methods=['GET', 'POST'])
def profile():

    if not 'username' in session:
        return redirect("/")

    if 'logout' in request.form:
            session.clear()
            return redirect('/')

    username = session["username"]
    bio = get_bio(username)

    blogIDs = get_blogs(username)
    if blogIDs[0] == 'None':
        blogIDs = blogIDs[1:]

    for ID in blogIDs:
        if f'{ID}' in request.form:
            session['blogid'] = f'{ID}'
            return redirect('/viewblog')
    
    blogs = [[blogIDs[i], get_blog_name(blogIDs[i]), username] for i in range(len(blogIDs))]

    return render_template("profile.html", username = username, bio=bio, blogs=blogs)


@app.route("/editpf", methods=['GET', 'POST'])
def editpf():
    style = url_for('static', filename='style.css')
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
                return render_template('editpf.html', username=session['username'], bio=get_bio(session['username']), error=e, url=style)

        if 'password_form' in request.form:
            try:
                change_password(session['username'], request.form['old_pass'], request.form['new_pass'])

            except ValueError as e:
                return render_template('editpf.html', username=session['username'], bio=get_bio(session['username']), error=e, url=style)

        if 'bio_form' in request.form:
            change_bio(session['username'], request.form['bio'])

        if 'logout' in request.form:
            session.clear()
            return redirect('/')

    return render_template('editpf.html', username=session['username'], bio=get_bio(session['username']), url=style)


@app.route("/viewblog", methods=['GET', 'POST'])
def viewblog():
    if not 'username' in session:
        return redirect("/")

    username = session["username"]

    entries = get_entries(blogid)

    if request.method == 'POST':
        for entryid in entries:
            if f'{entryid}' in request.form:
                return redirect(url_for('editntry', entryid=f'{entryid}'))

        if 'logout' in request.form:
            session.clear()
            return redirect('/')

    return render_template('viewblog.html', blogid=blogid, username=username)

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    style = url_for('static', filename='style.css')

    if not 'username' in session:
        return redirect("/")

    if 'logout' in request.form:
            session.clear()
            return redirect('/')

    username = session["username"]
    bio = get_bio(username)

    return render_template("profile.html", username = username, bio=bio, url=style)


if (__name__ == "__main__"):
    app.debug = True; # temporary!
    app.run()
