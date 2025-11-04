# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from datetime import datetime # for user signup date

import sqlite3   #enable control of an sqlite database

import secrets


DB_FILE="data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#=============================MAKE=TABLES=============================#

# make the database tables we need if they don't already exist

# userdata
c.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        username TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        sign_up_date DATE NOT NULL,
        bio TEXT,
        blog_ids TEXT
    )"""
)

# blogs
c.execute("""
    CREATE TABLE IF NOT EXISTS blogs (
        blog_name TEXT NOT NULL,
        blog_id TEXT PRIMARY KEY NOT NULL,
        author_username TEXT NOT NULL
    )"""
)

# entries
c.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        entry_name TEXT NOT NULL,
        entry_id TEXT PRIMARY KEY NOT NULL,
        blog_id TEXT NOT NULL,
        upload_date DATE NOT NULL,
        edit_date DATE NOT NULL,
        contents TEXT
    )"""
)

#=============================LOGIN=REGISTER=============================#

def user_exists(username):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    all_users = c.execute("SELECT username FROM userdata")
    for user in all_users:
        if (user[0] == username):
            db.commit()
            db.close()
            return True
    db.commit()
    db.close()
    return False

# RETURN VALUES ARE TEMPORARY
def register_user(username, password):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if user_exists(username):
        # throw error here
        db.commit()
        db.close()
        return "bad"
    # hash password here?
    # retrieve date in yyyy-mm-dd format
    date = datetime.today().strftime('%Y-%m-%d')
    c.execute(f'INSERT INTO userdata VALUES ("{username}", "{password}", {date}, NULL, NULL)')
    db.commit()
    db.close()
    return "success"

# RETURN VALUES ARE TEMPORARY
def auth(username, password):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if not user_exists(username):
        # throw some error here maybe?
        print("user dne")
        db.commit()
        db.close()
        return False
    # hash password here? (MUST MATCH other hash from register)
    real_pass = c.execute(f"SELECT password FROM userdata WHERE username = \"{username}\"")
    real_password = real_pass.fetchone()
    
    db.commit()
    db.close()
    
    return real_password[0] == password


#=============================BLOGS-ENTRIES=============================#

def gen_entry_id():
    # use secrets module to generate a random 32-byte string
    ID = secrets.token_hex(32)
    # make sure the ID really is unique
    # btw this will crash the app if there are enough users... but we'd need like 2^32 users sooo
    while entry_exists(ID):
        ID = secrets.token_hex(32)
    return ID

# helper
def entry_exists(entry_id):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    matching_entry = c.execute(f'SELECT * FROM entries WHERE entry_id = "{entry_id}"').fetchall()
    print(matching_entry)
    if len(matching_entry) > 0:
        db.commit()
        db.close()
        return True
    
    db.commit()
    db.close()
    return False

# add a *NEW* entry to a blog, return ID
def add_entry(entry_name, blog_id, contents):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    entry_id = gen_entry_id()
    # retrieve date in yyyy-mm-dd format
    date = datetime.today().strftime('%Y-%m-%d')
    c.execute(f'INSERT INTO entries VALUES ("{entry_name}", "{entry_id}", "{blog_id}", "{date}", "{date}", "{contents}")')
    
    db.commit()
    db.close()
    return entry_id

def update_entry(entry_id, contents):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    # get current list of stuff in the row
    old_data = c.execute(f'SELECT * FROM entries WHERE entry_id = "{entry_id}"').fetchall()
    print(old_data)
    
    db.commit()
    db.close()

# get all the entries associated with a certain blog
def get_entries(blog_id):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    entries = c.execute(f"SELECT entry_name FROM entries WHERE blog_id = \"{blog_id}").fetchall()
    print(entries)
    
    db.commit()
    db.close()


key = add_entry("test", "fakeblog", "hello these are the contents of the fake entry")
print(entry_exists(key))
print(key)
print(entry_exists("o"))

db.commit() #save changes
db.close()  #close database
