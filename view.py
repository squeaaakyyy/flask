from app import app
from flask import render_template
from posts.blueprint import *

@app.route('/')
def index():
    return render_template('index.html')
#
# @app.route('/')
# index()
