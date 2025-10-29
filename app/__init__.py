# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html');

@app.route("/home", methods=['GET','POST']) # will need to use post for password at the very least
def authenticate():
    if (request.method == "POST"):
        username = request.form.get('username','')
    else:
        username = request.args.get('username','')
    return render_template('home.html', username=username) 

@app.route("/register", methods=['GET', 'POST'])
def register():
    DB_FILE="data.db"

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    c.execute("CREATE TABLE IF NOT EXISTS userdata(username TEXT, password TEXT, sign_up_date TEXT, bio TEXT, blog_ids TEXT, PRIMARY KEY(username))")
    
    if request.method == 'POST':
        usernamedata = c.execute("SELECT username FROM userdata")
        for row in usernamedata:
            if row[0] == request.form['username']:
                print("BAD THINGS")
                #Throw error for same username
                
        #Needs value for sign_up_date
        c.execute(f"INSERT INTO userdata VALUES (\"{request.form['username']}\", \"{request.form['password']}\", \"\", \"\", \"\")")
        return redirect("/")

    return render_template('register.html')

if (__name__ == "__main__"):
    app.debug = True; # temporary!
    app.run()