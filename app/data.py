# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from datetime import datetime # for user signup date

import sqlite3   #enable control of an sqlite database


DB_FILE="data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#==========================================================

# make the database tables we need if they don't already exist

# userdata
c.execute("CREATE TABLE IF NOT EXISTS userdata(username TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL, sign_up_date DATE NOT NULL, bio TEXT, blog_ids TEXT);")
# blogs
c.execute("CREATE TABLE IF NOT EXISTS blogs(blog_name TEXT NOT NULL, blog_id TEXT PRIMARY KEY NOT NULL, author_username TEXT NOT NULL);")
# entries
c.execute("CREATE TABLE IF NOT EXISTS entries(entry_name TEXT NOT NULL, entry_id TEXT PRIMARY KEY NOT NULL, blog_id TEXT NOT NULL, upload_date DATE NOT NULL, edit_date DATE NOT NULL, contents TEXT);")
#docdata
c.execute("CREATE TABLE IF NOT EXISTS docdata(document TEXT PRIMARY KEY NOT NULL, creation_date DATE NOT NULL, bio TEXT, blog_ids TEXT);")
def user_exists(username):
    all_users = c.execute("SELECT username FROM userdata;").fetchall()
    for user in all_users:
        if (user[0] == username):
            return True
    return False

# RETURN VALUES ARE TEMPORARY
def register_user(username, password):
    if user_exists(username):
        # throw error here
        return "bad"
    # hash password here?
    # retrieve date it yyyy-mm-dd format
    date = datetime.today().strftime('%Y-%m-%d')
    c.execute(f'INSERT INTO userdata VALUES ("{username}", "{password}", {date}, NULL, NULL);')
    return "success"

# RETURN VALUES ARE TEMPORARY
def auth(username, password):
    if not user_exists(username):
        # throw some error here maybe?
        return "user doesn't exist"
    # hash password here? (MUST MATCH other hash from register)
    real_pass = c.execute(f"SELECT password FROM userdata WHERE username = {username};").fetchall()
    real_pass = real_pass[0]
    return real_pass == password

def doc_exists(docname, username):
    all_docs = c.execute("SELECT document FROM docdata;").fetchall()
    for doc in all_docs:
        if (doc[0] == document):
            return True
    return False

def post(docname):
    if doc_exists(docname):
        return "Document already exists"
    

db.commit() #save changes
db.close()  #close database