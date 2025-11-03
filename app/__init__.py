# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from flask import Flask, render_template, request

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


if (__name__ == "__main__"):
    app.debug = True; # temporary!
    app.run()
    
    