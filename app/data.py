# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

import sqlite3   #enable control of an sqlite database
import secrets  # used to generate ids
from datetime import datetime # for user signup date


#=============================MAKE=TABLES=============================#

# make the database tables we need if they don't already exist

# userdata
def create_user_data():
    
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS userdata (
            username TEXT PRIMARY KEY NOT NULL,
            password TEXT NOT NULL,
            sign_up_date DATE NOT NULL,
            bio TEXT,
            blog_ids TEXT
        )"""
    )
    
    db.commit()
    db.close()


# blogs
def create_blog_data():
    
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            blog_name TEXT NOT NULL,
            blog_id TEXT PRIMARY KEY NOT NULL,
            author_username TEXT NOT NULL
        )"""
    )
    
    db.commit()
    db.close()


# entries
def create_entry_data():
    
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
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
    
    db.commit()
    db.close()


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
    real_pass = c.execute(f'SELECT password FROM userdata WHERE username = "{username}"')
    real_password = real_pass.fetchone()
    
    db.commit()
    db.close()
    
    return real_password[0] == password



#=============================BLOGS=============================#


#----------BLOG-ACCESSORS----------#


# wrapper method
# get all the entry_ids associated with a certain blog
def get_entries(blog_id):
    return get_field_list('entries', 'blog_id', blog_id, 'entry_id')


#----------BLOG-MUTATORS----------#


# create a *NEW* blog, return ID
def new_blog(blog_name, author_username):
    
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    blog_id = gen_id()
    # make sure the id is unique
    while (blog_exists(blog_id)):
        blog_id = gen_id()
    
    c.execute(f'INSERT INTO blogs VALUES ("{blog_name}", "{blog_id}", "{author_username}")')
    
    db.commit()
    db.close()
    return blog_id


#----------BLOG-HELPERS----------#


# helper for new_blog
def blog_exists(blog_id):
    
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    matching_blog = c.execute(f'SELECT * FROM blogs WHERE blog_id = "{blog_id}"').fetchall()
    if len(matching_blog) > 0:
        db.commit()
        db.close()
        return True
    
    db.commit()
    db.close()
    return False


#=============================ENTRIES=============================#


#----------ENTRY-ACCESSORS----------#


# wrapper method
def get_entry_name(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'entry_name')

# wrapper method
def get_entry_blog(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'blog_id')

# wrapper method
def get_entry_udate(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'upload_date')

# wrapper method
def get_entry_edate(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'edit_date')

# wrapper method
def get_entry_contents(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'contents')

# returns a list of every field associated with this entry_id (besides the id itself)
# wrapper method
def get_entry_all(entry_id):
    return get_all_fields('entries', 'entry_id', entry_id)


#----------ENTRY-MUTATORS----------#


# add a *NEW* entry to a blog, return ID
def add_entry(entry_name, blog_id, contents):
    
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    entry_id = gen_id()
    # make sure the id is unique
    while (entry_exists(entry_id)):
        entry_id = gen_id()
    
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


# helper for add_entry
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


# generate an id
def gen_id():
    # use secrets module to generate a random 32-byte string
    return secrets.token_hex(32)


# used for a bunch of accessor methods; used when only 1 item should be returned
def get_field(table, ID_fieldname, ID, field):
    
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    data = c.execute(f'SELECT {field} FROM {table} WHERE {ID_fieldname} = "{ID}"').fetchone()
    
    db.commit()
    db.close()
    
    return data[0]


# used for a bunch of accessor methods; used when a list of items in a certain field should be returned
def get_field_list(table, ID_fieldname, ID, field):
    
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    data = c.execute(f'SELECT {field} FROM {table} WHERE {ID_fieldname} = "{ID}"').fetchall()
    
    db.commit()
    db.close()
    
    return clean_list(data)


# returns a list of every field associated with this id (including the id itself)
def get_all_fields(table, ID_fieldname, ID):
    
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    data = c.execute(f'SELECT * FROM {table} WHERE {ID_fieldname} = "{ID}"').fetchall()
    
    db.commit()
    db.close()
    
    return clean_list(data)


# turn a list of tuples (returned by .fetchall()) into a 1d list
def clean_list(raw_output):
    
    #clean_output = [raw_output[i][0] for i in range(len(raw_output))]
    
    clean_output = []
    for lst in raw_output:
        for item in lst:
            clean_output += [item]
    
    return clean_output


#=============================MAIN=SCRIPT=============================#

# make tables
create_user_data()
create_blog_data()
create_entry_data()


blog1 = new_blog("blog1", "maya")
key1 = add_entry("entry1", blog1, "contents1")
update_entry(key1, "updateentry1", "updatecontents1")
key2 = add_entry("entry2", blog1, "contents2")
print(get_entry_all(key1))
print(get_entry_udate(key2))
print(get_entries(blog1))

