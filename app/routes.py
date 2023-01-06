from app import app
import os
import requests
from flask import render_template, url_for, request, redirect, flash, send_file, session
from flask_paginate import Pagination, get_page_args
import math
import logging
logging.basicConfig(level=logging.DEBUG)

# from Image import convert_to_binary


# Constants
RES_PER_PAGE = 10


@app.route('/')
@app.route('/index')
def index():
    images = [f'images/{img}' for img in os.listdir('app/static/images')]
    return render_template('index.html', images=images)


@app.route('/show_image/<image_name>')
def show_image(image_name):
    images = [f'images/{img}' for img in os.listdir('app/static/images')]
    original_order = images
    session['original_order'] = original_order # Sets the original order of all the images
    return render_template('show_image.html', images=images, image=f'images/{image_name}')


@app.route('/intensity/<filename>')
def get_intensity(filename):
    """
    Gets the intensity of the image
    Pass the order of the array using sessions, then sort

    Args:
        filename (_type_): Filename of the image
    """
    """ TODO Code for getting INTENSITY and ordering the images goes here!!!"""
    """ Place the ordered list of images in the session """
    return redirect(url_for('results', filename=filename))


@app.route('/colorCode/<filename>')
def get_color_code(filename):
    """
    Gets the intensity of the image
    Pass the order of the array using sessions, then sort

    Args:
        filename (_type_): Filename of the image
    """
    print(filename)
    """ TODO Code for getting color code and ordering the images goes here!!!"""
    """ Place the ordered list of images in the session """
    return redirect(url_for('results', filename=filename))


@app.route('/results/<filename>')
def results(filename):
    """
    Displays the actual data

    Args:
        filename (_type_): The filename for unique identifiers

    Returns:
        _type_: The template that orders the images
    """
    print('this was "sorted"!')
    print(filename)
    filename = filename.replace('?', '/')
    images = session.get('images', [])
    print(session.get('original_order'))
    if images == []: # If there was an error with getting sessions data
        return redirect(url_for('index'))
    else:
        return render_template('sorted.html', filename=filename)




# -------------- API ----------------


@app.route('/get_image/<image_name>')
def getImage(image_name):
    # request.headers["content-type"] = "image/png"
    files = os.listdir('app/static/images')
    if image_name in files:
        return send_file(f'static/images/{image_name}', 'image/png')
    else:
        return "Image not found", 404


@app.route('/get_image/<image_name>/binary')
def getImageBinary(image_name):
    """ TODO in part 2
    Gets the Binary of the image

    Args:
        image_name (_type_): _description_
    """
    ...


@app.route('/get_image/all')
def getAllImages():
    """
    Gets all the images names
    You can pull the images after that
    """
    ...


# Helper Functions for simplicity
def _convert_to_binary(self, num):
    return bin(n).replace("0b", "")
