# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

import sqlite3   #enable control of an sqlite database
import secrets  # used to generate ids
from datetime import datetime # for user signup date
import hashlib   #for consistent hashes


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


#=============================USERDATA=============================#


#----------USERDATA-ACCESSORS----------#


def get_sign_up_date(username):
    return get_field('userdata', 'username', username, 'sign_up_date')


def get_bio(username):
    return get_field('userdata', 'username', username, 'bio')


def get_blogs(username):
    # blog ids are stored as text; split the string (delimiter = space)
    # cut the first item, which is 'None'
    return get_field('userdata', 'username', username, 'blog_ids').split(' ')[1:]


#----------USERDATA-MUTATORS----------#


# FUNCTIONAL BUT MORE STUFF TBA
# adds a new user's data to user table
def register_user(username, password):

    if user_exists(username):
        # throw error here
        return "bad"

    # hash password here?
    # retrieve date in yyyy-mm-dd format
    date = datetime.today().strftime('%Y-%m-%d')

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    password = password.encode('utf-8')
    password = str(hashlib.sha256(password).hexdigest())

    c.execute(f'INSERT INTO userdata VALUES ("{username}", "{password}", "{date}", NULL, NULL)')

    db.commit()
    db.close()

    return "success"


# FUNCTIONAL BUT MORE STUFF TBA
def change_username(old_username, new_username):

    if user_exists(new_username):
        # throw error here
        return "bad"

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # update stuff associated with old username
    c.execute(f'UPDATE blogs SET author_username = "{new_username}" WHERE username = "{old_username}"')
    c.execute(f'UPDATE userdata SET username = "{new_username}" WHERE username = "{old_username}"')

    db.commit()
    db.close()

    return "success"


# FUNCTIONAL BUT MORE STUFF TBA
def change_password(username, old_pass, new_pass):

    if not auth(username, old_pass):
        return "bad"

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    old_pass = old_pass.encode('utf-8')
    old_pass = str(hashlib.sha256(old_pass).hexdigest())
    new_pass = new_pass.endcode('utf-8')
    new_pass = str(hashlib.sha256(new_pass).hexdigest())

    c.execute(f'UPDATE userdata SET password = "{new_pass}" WHERE username = "{username}"')

    db.commit()
    db.close()

    return "success"


def change_bio(username, contents):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # get current list of stuff in the row
    c.execute(f'UPDATE userdata SET bio = "{contents}" WHERE username = "{username}"')

    db.commit()
    db.close()


def add_blog(blog_name, author_username):

    blog_id = new_blog(blog_name, author_username)
    other_blogs = get_field('userdata', 'username', author_username, 'blog_ids')

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # get current list of stuff in the row
    c.execute(f'UPDATE userdata SET blog_ids = "{other_blogs} {blog_id}" WHERE username = "{author_username}"')

    db.commit()
    db.close()

    return blog_id


#----------USERDATA-HELPERS----------#


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
    passpointer = c.execute(f'SELECT password FROM userdata WHERE username = "{username}"')
    real_pass = passpointer.fetchone()[0]

    db.commit()
    db.close()

    password = password.encode('utf-8')

    print(real_pass + ', ' + str(hashlib.sha256(password).hexdigest()))
    return real_pass == str(hashlib.sha256(password).hexdigest())



#=============================BLOGS=============================#


#----------BLOG-ACCESSORS----------#


# get all the entry_ids associated with a certain blog
def get_entries(blog_id):
    return get_field_list('entries', 'blog_id', blog_id, 'entry_id')


# get all blogs
def get_blogs():

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute(f'SELECT blog_id FROM blogs').fetchall()

    db.commit()
    db.close()

    return clean_list(data)


def get_blog_name(blog_id):
    return get_field("blogs", "blog_id", blog_id, blog_name)


def get_blog_author(blog_id):
    return get_field("blogs", "blog_id", blog_id, author_username)


#----------BLOG-MUTATORS----------#


# **YOU SHOULDN'T BE USING THIS** see add_blog in userdata section
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


# delete blog?


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


def get_entry_name(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'entry_name')


def get_entry_blog(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'blog_id')


def get_entry_udate(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'upload_date')


def get_entry_edate(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'edit_date')


def get_entry_contents(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'contents')


# returns a list of every field associated with this entry_id (besides the id itself)
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


# delete entry?


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
    return get_field_list(table, ID_fieldname, ID, field)[0]


# wrapper method
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
