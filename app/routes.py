from app import app
import os
from flask import render_template, url_for, request, redirect, session
from PIL import Image
from collections import defaultdict
from flask_paginate import Pagination

# NOTE TESTING ONLY if you want to refresh your session constantly
# app.secret_key = os.urandom(32)
# np.set_printoptions(threshold=np.inf)

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
    images = [f'images/{img}' for img in os.listdir('app/static/images')]

    # Pagination
    def get_page_image(offset=0, per_page=20):
        return images[offset: offset + per_page]
    # page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    pagination_images = get_page_image(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=len(images), css_framework='bulma')

    imageList = defaultdict(list)
    if not session.get('original_order'):
        original_order = images
        # Sets the original order of all the images
        session['original_order'] = original_order
    # Gets the image list + all of the intensity and Cc values
    if not session.get('imageList'):
        # Loops through all the images in the folder
        for image in os.listdir('app/static/images'):
            # Gets relative image path
            imagePath = f'app/static/images/{image}'
            # Opens the image using PIL
            im = Image.open(imagePath)
            # Grabs the individual RGB Pixel data
            pixels = list(im.getdata())
            # Encode all of the pixels into bins called CcBin and InBin
            CcBin, InBin = encode(pixels)
            imageList[image] = {
                'bins': [InBin, CcBin],  # Get the bins for the image
                # Get number of pixels in an image
                'size': len(pixels)
            }
        session['imageList'] = imageList  # Saves bins to sessions
    # print(session.get('imageList')['1.jpg']) # Testing. if you wanna see 1.jpg's features, uncomment this out
    return render_template('index.html', images=pagination_images, page=page, per_page=20, pagination=pagination)


@app.route('/show_image/<image_name>')
def show_image(image_name):
    """Shows the image in its own page

    Args:
        image_name (_type_): The image name

    Returns:
        template (_type_): HTML template of the image page
    """
    return render_template('show_image.html', image=f'images/{image_name}')


@app.route('/intensity/<filename>')
def get_intensity(filename):
    """
    Gets the intensity of the image
    Pass the order of the array using sessions, then sort

    Args:
        filename (_type_): Filename of the image
    """
    # print(session.get('imageList'))
    # print(f'will this work? image {filename}', session.get('imageList')[filename.split('?')[1]])
    target_image = filename.split('?')[1]  # Target Image fully parsed from URL
    sortedList = []
    # Use Manhatten distance to sort the images based on Intensity
    for image in session.get('imageList').keys():
        get_distance = manhattanDistance(target_image, image, 'I')
        # Append the image and the distance of the image compared to the target_image
        sortedList.append((get_distance, image))
    # Sort the list based on the intensity
    sortedList = sorted(sortedList, key=lambda x: x[0])
    session['sortedList'] = sortedList

    return redirect(url_for('results', filename=filename))


@app.route('/colorCode/<filename>')
def get_color_code(filename):
    """
    Gets the intensity of the image
    Pass the order of the array using sessions, then sort

    Args:
        filename (_type_): Filename of the image
    """
    target_image = filename.split('?')[1]  # Target Image fully parsed from URL
    sortedList = []
    # Use Manhatten distance to sort the images based on CC
    for image in session.get('imageList').keys():
        get_distance = manhattanDistance(target_image, image, 'CC')
        # Append the image and the distance of the image compared to the target_image
        sortedList.append((get_distance, image))
    # Sort the list based on the Color code
    sortedList = sorted(sortedList, key=lambda x: x[0])
    session['sortedList'] = sortedList
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
    filename = filename.replace('?', '/')
    if session.get('sortedList') == []:
        return redirect(url_for('index'))
    # Grabs the sorted list values from the session
    final_list = session.get('sortedList')
    final_list = [f'images/{img[1]}' for img in final_list]
    # Pagination support for results page
    def get_page_image(offset=0, per_page=20):
        return final_list[offset: offset + per_page]
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    pagination_images = get_page_image(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=len(final_list), css_framework='bulma')
    return render_template('sorted.html', images=pagination_images, page=page, per_page=20, pagination=pagination)


def encode(pixList):
    """The encode function for finding the bins.
    This function stores all of the bins for the image and the index route will cache them in cookies
    for faster lookup times. When we want to access these Intensity and CC bins for comparison
    We can instantly look them up, since they won't change

    Args:
        pixList (_type_): Pixel list

    Returns:
        _type_: Returns Color Code and Intensity bin for image
    """
    CcBins = [0]*64
    InBins = [0]*25
    # Encode the image
    pixList = list(pixList)
    for pix in pixList:
        # Find the Intensity
        intensity = (0.299*pix[0]) + (0.587*pix[1]) + (0.114*pix[2])
        # Increments bin[int((intensity // 10) % 25)] inside of the bin
        if intensity < 250:
            InBins[int((intensity // 10))] += 1
        else:
            # Edge case for 250 - 255 to place in last bin (bin 24)
            InBins[int((intensity // 10) - 1)] += 1

        # Color code converts rgb value to binary
        v1, v2, v3 = _convert_to_binary(pix[0]), _convert_to_binary(
            pix[1]), _convert_to_binary(pix[2])
        # Converts to 6 digit binary, ensuring that the change isn't transparent from the value
        v1, v2, v3 = v1.rjust((8-len(v1)) + len(v1), '0')[:2], v2.rjust(
            (8-len(v2)) + len(v2), '0')[:2], v3.rjust((8-len(v3)) + len(v3), '0')[:2]
        six_digit_code = str(v1) + str(v2) + str(v3)
        # Convert binary to decimal, then increment the bin based on the decimal
        CcBins[int(six_digit_code, 2)] += 1

    return CcBins, InBins


def manhattanDistance(target, image, type):
    """
    Calculates the manhattan distance between the target and the image

    Args:
        target (_type_): The target image filename
        image (_type_): The image to be compared to the target filename

    Returns:
        _type_: The manhattan distance between the two images
    """
    distance = 0
    target_size = session.get('imageList')[target]['size']
    image_size = session.get('imageList')[image]['size']
    target_bin = []
    image_bin = []
    # handles Intensity values
    if type == 'I':
        # Gets the intensity bin for the target image
        target_bin = session.get('imageList')[target]['bins'][0]
        image_bin = session.get('imageList')[image]['bins'][0]
        # Loop through the different bins of both the target and image that is being compared
    # Handles Color Code values
    elif type == 'CC':
        # Gets the color code bin for the target image
        target_bin = session.get('imageList')[target]['bins'][1]
        image_bin = session.get('imageList')[image]['bins'][1]
    else:  # Error
        return -1
    # Loops through all the binned proportions and calculates using Manhattan distance
    for i in range(len(target_bin)):
        distance += abs(((target_bin[i]) / (target_size)
                         ) - (image_bin[i] / (image_size)))
    return distance


# Helper Functions for simplicity
def _convert_to_binary(num):
    return bin(num).replace("0b", "")
