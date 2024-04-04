from . import app
from .controller.AppController import AppController
from flask import render_template


@app.route('/')
def main():
    return render_template('main.html')

@app.route("/classify", methods=['POST'])
def get_result():
    return AppController().get_result()

@app.route("/clear-image", methods=['POST'])
def clear_image():
    return AppController().clearImage()