# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from datetime import datetime # for user signup date

import sqlite3   #enable control of an sqlite database


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
    # retrieve date it yyyy-mm-dd format
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
    print(real_password)
    db.commit()
    db.close()
    return real_password[0] == password

db.commit() #save changes
db.close()  #close database