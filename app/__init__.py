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
            return redirect(url_for('viewblog', blogid=ID))

    blog_info = [[blog_keys[i], get_blog_name(blog_keys[i]), get_blog_author(blog_keys[i])] for i in range(len(blog_keys))]

    return render_template('home.html', username=username, blogs=blog_info, url=style)


@app.route("/viewblog/<string:blogid>", methods=['GET', 'POST'])
def viewblog(blogid):
    if not 'username' in session:
        return redirect("/")
    
    if 'logout' in request.form:
        session.clear()
        return redirect('/')
    
    if request.method == 'POST':
        for entryid in get_entries(blogid):
            if f'{entryid}' in request.form:
                return redirect(url_for('editntry', entryid=f'{entryid}'))
            
        if 'add_entry' in request.form:
            entry_id = add_entry("Untitled Entry", blogid, "")
            return redirect(url_for('editntry', entryid=entry_id))
    
    entrynames = []
    entrycontents = []
    entryudates = []
    entryedates = []
    for entry in get_entries(blogid):
        entrynames.append(get_entry_name(entry))
        entrycontents.append(get_entry_contents(entry))
        entryudates.append(get_entry_udate(entry))
        entryedates.append(get_entry_edate(entry))
    
    return render_template('viewblog.html', username=session['username'], length=len(entrynames), blog_name=get_blog_name(blogid), blog_author=get_blog_author(blogid), entry_ids=get_entries(blogid), entry_names=entrynames, entry_contents=entrycontents, entry_udates=entryudates, entry_edates=entryedates)


@app.route("/newblog", methods=['GET', 'POST'])
def newblog(): 
    if not 'username' in session:
        return redirect("/")

    if 'logout' in request.form:
        session.clear()
        return redirect('/')

    username = session["username"]

    if request.method == 'POST':
        if 'newblog_title' in request.form:
            try:
                ID = add_blog(request.form['blogname'], session['username'])
                return redirect(url_for('viewblog', blogid=ID))
            except ValueError as e:
                return render_template('newblog.html', username=session['username'], error=e)

    return render_template('newblog.html', username=session['username'])


@app.route("/editntry/<string:entryid>", methods=['GET', 'POST'])
def editntry(entryid):
    if not 'username' in session:
        return redirect("/")

    if 'logout' in request.form:
        session.clear()
        return redirect('/')
    
    if request.method == 'POST':
        update_entry(entryid, request.form['entry_name'], request.form['entry_contents'])
        return redirect(url_for('viewblog', blogid=get_entry_blog(entryid)))
        
    return render_template("editntry.html", entry_id=entryid, blog_name=get_blog_name(get_entry_blog(entryid)), entry_name=get_entry_name(entryid), entry_contents=get_entry_contents(entryid))

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
    
    if 'logout' in request.form:
            session.clear()
            return redirect('/')

    if request.method == 'POST':
        if 'username_form' in request.form:
            try:
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

    return render_template('editpf.html', username=session['username'], bio=get_bio(session['username']))


if (__name__ == "__main__"):
    app.debug = True; # temporary!
    app.run()
