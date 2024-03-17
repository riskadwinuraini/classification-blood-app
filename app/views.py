from . import app
from .controller.AppController import AppController
from flask import render_template


@app.route('/')
def main():
    return render_template('main.html')

@app.route("/submit", methods=['POST'])
def submit():    
    return AppController().get_output()

