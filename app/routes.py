from app import app
import os
from flask import render_template, url_for, request, redirect, session
from PIL import Image
from collections import defaultdict
from flask_paginate import Pagination
import numpy as np
import math

# NOTE TESTING ONLY if you want to refresh your session constantly
app.secret_key = os.urandom(32)
np.set_printoptions(threshold=np.inf)


@app.route('/')
@app.route('/index')
def index():
    """The index page of the app.
    This page will show all the images in the folder, and it will also do the binning of the images and feature extraction.
    The reason why it will render so slowly if you run it manually, is that it will be looping through all the images and the individual pixels in each image.
    After that, it caches it into local storage. Make sure you don't change the SECRET_KEY, or else it will reset the cache, unless that's what you're trying to do.

    Returns:
        render_template (_type__): HTML template of the index page
    """
    return render_template('index.html')
