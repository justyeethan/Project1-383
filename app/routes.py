from app import app
import os
import requests
from flask import render_template, url_for, request, redirect, flash, send_file, session
import math
from PIL import Image
from collections import defaultdict

# TESTING ONLY TODO DELETE THIS LINE OF CODE
# app.secret_key = os.urandom(32)


@app.route('/')
@app.route('/index')
def index():
    images = [f'images/{img}' for img in os.listdir('app/static/images')]
    # key: image_name { value: [intensity, colorCode] }
    imageList = defaultdict(list)
    if not session.get('original_order'):
        original_order = images
        # Sets the original order of all the images
        session['original_order'] = original_order
    # Gets the image list + all of the intensity and Cc values
    if not session.get('imageList'):
        print('list not in session')
        for image in os.listdir('app/static/images'):
            imagePath = f'app/static/images/{image}'
            im = Image.open(imagePath)
            CcBin, InBin = encode(im.getdata())
            imageList[image] = {
                'bins': [InBin, CcBin],  # Get the bins for the image
                # Get number of pixels in an image
                'size': len(list(im.getdata()))
            }
        session['imageList'] = imageList  # Incodes values to sessions
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
    target_image = filename.split('?')[1]  # Target Image fully parsed from URL
    sortedList = []
    # TODO Use Manhatten distance to sort the images based on Intensity
    for image in session.get('imageList').keys():
        get_distance = manhattanDistance(target_image, image, 'CC')
        # Append the image and the distance of the image compared to the target_image
        sortedList.append((get_distance, image))
    sortedList = sorted(sortedList, key=lambda x: x[0])
    print(sortedList)
    session['sortedList'] = sortedList

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
    target_image = filename.split('?')[1]  # Target Image fully parsed from URL
    # print(filename, targetColorCode)
    sortedList = []
    # TODO Use Manhatten distance to sort the images based on CC
    for image in session.get('imageList').keys():
        print(image)
        get_distance = manhattanDistance(target_image, image, 'I')
        # Append the image and the distance of the image compared to the target_image
        sortedList.append((get_distance, image))
    sortedList = sorted(sortedList, key=lambda x: x[0])
    print(sortedList)
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
    # print('this was "sorted"!')
    # print(filename)
    filename = filename.replace('?', '/')
    # print(session.get('original_order'))
    if session.get('sortedList') == []:
        return redirect(url_for('index'))
    final_list = session.get('sortedList')
    final_list = [f'images/{img[1]}' for img in final_list]
    return render_template('sorted.html', images=final_list)


def encode(pixList):
    CcBins = [0]*64
    InBins = [0]*25
    # TODO Encode the image
    pixList = list(pixList)
    # print(pixList[0])
    for pix in pixList:
        # Intensity
        # Intensity = 0.2999R + 0.587G + 0.114B
        intensity = (0.2999*pix[0]) + (0.587*pix[1]) + (0.114*pix[2])
        # print(f'{pix}: {intensity}')
        # print(intensity, int((intensity // 10) % 25) + 1)
        # Increments bin[int((intensity // 10) % 25)] inside of the bin
        InBins[int((intensity // 10) % 25)] += 1

        # Color code
        # print(_convert_to_binary(pix[0]), _convert_to_binary(pix[1]), _convert_to_binary(pix[2]))
        six_digit_code = str(_convert_to_binary(pix[0]))[
            :2] + str(_convert_to_binary(pix[1]))[:2] + str(_convert_to_binary(pix[2]))[:2]
        # print(int(six_digit_code, 2))
        # Convert binary to decimal, then increment the bin based on the decimal
        CcBins[int(six_digit_code, 2)] += 1

    # print(InBins)
    # print(CcBins)
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
    # TODO Calculate the manhattan distance between the target and the image
    # handles Intensity values
    distance = 0
    target_size = session.get('imageList')[target]['size']
    image_size = session.get('imageList')[image]['size']
    if type == 'I':
        target_bin = session.get('imageList')[target]['bins'][0]
        image_bin = session.get('imageList')[image]['bins'][0]
        # Loop through the different bins of both the target and image that is being compared
        for i in range(25):
            distance += abs(((target_bin[i]) / (target_size)
                             ) - (image_bin[i] / (image_size)))
    elif type == 'CC':
        target_bin = session.get('imageList')[target]['bins'][1]
        image_bin = session.get('imageList')[image]['bins'][1]
        for i in range(64):
            distance += abs(((target_bin[i]) / (target_size)
                             ) - (image_bin[i] / (image_size)))
    else:
        return -1
    return distance


# Helper Functions for simplicity
def _convert_to_binary(num):
    return bin(num).replace("0b", "")
