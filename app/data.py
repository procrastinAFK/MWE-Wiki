# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from datetime import datetime # for user signup date

import sqlite3   #enable control of an sqlite database

import secrets  # used to generate ids


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


# returns whether or not a user exists
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


# FUNCTIONAL BUT MORE STUFF TBA
# adds a new user's data to user table
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


# FUNCTIONAL BUT MORE STUFF TBA
# checks if provided password in login attempt matches user password
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



#=============================BLOGS-ENTRIES-MAIN=============================#


#----------ENTRY-ACCESSORS----------#


# get all the entries associated with a certain blog
def get_entries(blog_id):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    entries = c.execute(f'SELECT entry_id FROM entries WHERE blog_id = "{blog_id}"').fetchall()
    
    db.commit()
    db.close()
    
    # extract values from tuples so we can just return a 1d list
    return clean_list(entries)

# wrapper method
def get_entry_name(entry_id):
    return get_entry_field(entry_id, 'entry_name')

# wrapper method
def get_entry_blog(entry_id):
    return get_entry_field(entry_id, 'blog_id')

# wrapper method
def get_entry_udate(entry_id):
    return get_entry_field(entry_id, 'upload_date')

# wrapper method
def get_entry_edate(entry_id):
    return get_entry_field(entry_id, 'edit_date')

# wrapper method
def get_entry_contents(entry_id):
    return get_entry_field(entry_id, 'contents')

# returns a list of every field associated with this entry_id (besides the id itself)
def get_entry_all(entry_id):
    data = []
    data += [get_entry_field(entry_id, 'entry_name')]
    data += [get_entry_field(entry_id, 'blog_id')]
    data += [get_entry_field(entry_id, 'upload_date')]
    data += [get_entry_field(entry_id, 'edit_date')]
    data += [get_entry_field(entry_id, 'contents')]
    return data


#----------ENTRY-MUTATORS----------#


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


# modify the entry_name and/or entry's contents
def update_entry(entry_id, entry_name, contents):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    # get current list of stuff in the row
    c.execute(f'UPDATE entries SET entry_name = "{entry_name}", contents = "{contents}" WHERE entry_id = "{entry_id}"')
    
    db.commit()
    db.close()


#----------ENTRY-HELPERS----------#

# generate an id for a new entry
def gen_entry_id():
    # use secrets module to generate a random 32-byte string
    ID = secrets.token_hex(32)
    # make sure the ID really is unique
    # btw this will crash the app if there are enough users... but we'd need like 2^32 users sooo
    while entry_exists(ID):
        ID = secrets.token_hex(32)
    return ID


# used for a bunch of accessor methods above
def get_entry_field(entry_id, field):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    data = c.execute(f'SELECT {field} FROM entries WHERE entry_id = "{entry_id}"').fetchone()
    
    db.commit()
    db.close()
    return data[0]


# helper for gen_entry_id
def entry_exists(entry_id):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    matching_entry = c.execute(f'SELECT * FROM entries WHERE entry_id = "{entry_id}"').fetchall()
    if len(matching_entry) > 0:
        db.commit()
        db.close()
        return True
    
    db.commit()
    db.close()
    return False



#=============================GENERAL=HELPERS=============================#


# turn a list of tuples (returned by .fetchall()) into a 1d list
def clean_list(raw_output):
    clean_output = [raw_output[i][0] for i in range(len(raw_output))]
    return clean_output


#=============================FILE=END=============================#


db.commit() #save changes
db.close()  #close database
