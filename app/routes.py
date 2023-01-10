from app import app
import os
import requests
from flask import render_template, url_for, request, redirect, flash, send_file, session
from flask_paginate import Pagination, get_page_args
import math
from PIL import Image
from collections import defaultdict

# from Image import convert_to_binary


@app.route('/')
@app.route('/index')
def index():
    # app.secret_key = os.urandom(32) # TESTING ONLY TODO DELETE THIS LINE OF CODE
    images = [f'images/{img}' for img in os.listdir('app/static/images')]
    imageList = defaultdict(list) # key: image_name { value: [intensity, colorCode] }
    if not session.get('original_order'):
        original_order = images
        session['original_order'] = original_order # Sets the original order of all the images
    # Gets the image list + all of the intensity and Cc values
    if session.get('imageList'):
        print('list not in session')
        for image in os.listdir('app/static/images'):
            imagePath = f'app/static/images/{image}'
            im = Image.open(imagePath)
            CcBin, InBin = encode(im.getdata())
            imageList[image] = [InBin, CcBin]
        session['imageList'] = imageList # Incodes values to sessions
    else:
        # print(session['imageList'])
        ...
    return render_template('index.html', images=images)


@app.route('/show_image/<image_name>')
def show_image(image_name):
    return render_template('show_image.html', image=f'images/{image_name}')


@app.route('/intensity/<filename>')
def get_intensity(filename):
    """
    Gets the intensity of the image
    Pass the order of the array using sessions, then sort

    TODO
    - Code for getting INTENSITY and ordering the images goes here!
    - Create an indexable array of the images and their intensities, then save to sessions to save on compute time
    - Place the ordered list of images in the session
    - Sort the files based on the closest images to the current filename's intensity

    Args:
        filename (_type_): Filename of the image
    """
    # print(session.get('imageList'))
    # print(f'will this work? image {filename}', session.get('imageList')[filename.split('?')[1]])
    targetIntensity = session.get('imageList')[filename.split('?')[1]][0]
    print(filename, targetIntensity)
    sortedList = []

    return redirect(url_for('results', filename=filename))


@app.route('/colorCode/<filename>')
def get_color_code(filename):
    """
    Gets the intensity of the image
    Pass the order of the array using sessions, then sort
    TODO
    - Code for getting color code and ordering the images goes here!!!
    - Place the ordered list of images in the session

    Args:
        filename (_type_): Filename of the image
    """
    targetColorCode = session.get('imageList')[filename.split('?')[1]][1]
    print(filename, targetColorCode)
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
    print(session.get('original_order'))
    return render_template('sorted.html', images_ordered=[])


def encode(pixList):
    CcBins = [0]*64
    InBins = [0]*25
    # TODO Encode the image
    pixList = list(pixList)
    # print(pixList[0])
    for pix in pixList:
        # Intensity
        intensity = (0.2999*pix[0]) + (0.587*pix[1]) + (0.114*pix[2]) # Intensity = 0.2999R + 0.587G + 0.114B
        # print(f'{pix}: {intensity}')
        # print(intensity, int((intensity // 10) % 25) + 1)
        InBins[int((intensity // 10) % 25)] += 1 # Increments bin[int((intensity // 10) % 25)] inside of the bin

        # Color code
        # print(_convert_to_binary(pix[0]), _convert_to_binary(pix[1]), _convert_to_binary(pix[2]))
        six_digit_code = str(_convert_to_binary(pix[0]))[:2] + str(_convert_to_binary(pix[1]))[:2] + str(_convert_to_binary(pix[2]))[:2]
        # print(int(six_digit_code, 2))
        CcBins[int(six_digit_code, 2)] += 1

    # print(InBins)
    # print(CcBins)
    return CcBins, InBins


# Helper Functions for simplicity
def _convert_to_binary(num):
    return bin(num).replace("0b", "")
