from app import app
import os
import requests
from flask import render_template, url_for, request, redirect, flash
from flask_paginate import Pagination, get_page_args
import math

# from Image import convert_to_binary


# Constants
RES_PER_PAGE = 10


@app.route('/')
@app.route('/index')
def index():
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    images = [f'images/{img}' for img in os.listdir('app/static/images')]
    total = len(images)
    pagination_images = images[offset:offset+RES_PER_PAGE]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    # return render_template('index.html', images=images, image='images/1.jpg', pagination=pagination)
    return render_template('index.html', images=pagination_images, page=page, image='images/1.jpg', per_page=per_page, pagination=pagination)


@app.route('/show_image/<image_name>')
def show_image(image_name):
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    images = [f'images/{img}' for img in os.listdir('app/static/images')]
    total = len(images)
    pagination_images = images[offset:offset+RES_PER_PAGE]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    # return render_template('index.html', images=images, image=f'images/{image_name}')
    return render_template('index.html', images=pagination_images, page=page, image=f'images/{image_name}', per_page=per_page, pagination=pagination)

# @app.route('/view_image/<image_name>')
# def view_image(image_name):
#     return send_from_directory(f'app/static/images/{image_name}')




# Helper Functions for simplicity
def _convert_to_binary(self, num):
    return bin(n).replace("0b", "")