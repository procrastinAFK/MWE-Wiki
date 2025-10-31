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
    all_users = c.execute("SELECT username FROM userdata").fetchall()
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
    c.execute(f'INSERT INTO userdata VALUES ("{username}", "{password}", {date}, NULL, NULL)')
    return "success"

# RETURN VALUES ARE TEMPORARY
def auth(username, password):
    if not user_exists(username):
        # throw some error here maybe?
        return "user doesn't exist"
    # hash password here? (MUST MATCH other hash from register)
    real_pass = c.execute(f'SELECT password FROM userdata WHERE username = "{username}"').fetchall()
    # WHY
    real_pass = real_pass[0][0]
    print(real_pass)
    return real_pass == password

print(auth("tester","abc"))
print(auth("tester","ab"))
print(auth("tesrrter","abc"))
print(c.execute("SELECT * FROM userdata").fetchall())
db.commit() #save changes
db.close()  #close database