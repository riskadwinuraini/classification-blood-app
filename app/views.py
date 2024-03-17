from . import app
from .controller.AppController import AppController
from flask import render_template


@app.route('/')
def main():
    return render_template('main.html')

@app.route("/tmp", methods=['POST'])
def temporary():    
    return AppController().tmp()

@app.route("/classify", methods=['POST'])
def get_result():
    return AppController().get_result()