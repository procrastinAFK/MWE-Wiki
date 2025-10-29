# MWE (Maya Berchin, Ashley Li, Evan Khosh, Robert Chen)
# p00
# Softdev

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html');

if (__name__ == "__main__"):
    app.debug = True; # temporary!
    app.run()