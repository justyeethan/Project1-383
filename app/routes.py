from app import app
import os
from flask import render_template, url_for, request, redirect, flash, send_file, session
import numpy as np
from PIL import Image
from collections import defaultdict

# TESTING ONLY TODO DELETE THIS LINE OF CODE
app.secret_key = os.urandom(32)
np.set_printoptions(threshold=np.inf)


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
            pixels = list(im.getdata())
            width, height = im.size
            # print(width * height)
            # pixels = np.array([pixels[i * width:(i + 1) * width] for i in range(height)])
            # print(pixels)
            CcBin, InBin = encode(pixels)
            imageList[image] = {
                'bins': [InBin, CcBin],  # Get the bins for the image
                # Get number of pixels in an image
                'size': len(pixels)
                # 'size': width * height
            }
        session['imageList'] = imageList  # Incodes values to sessions
    print(session.get('imageList')['1.jpg'])
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
        get_distance = manhattanDistance(target_image, image, 'I')
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
        get_distance = manhattanDistance(target_image, image, 'CC')
        # Append the image and the distance of the image compared to the target_image
        sortedList.append((get_distance, image))
    sortedList = sorted(sortedList, key=lambda x: x[0])
    # print(sortedList)
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
    # print(final_list)
    final_list = [f'images/{img[1]}' for img in final_list]
    return render_template('sorted.html', images=final_list)


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
    # TODO Encode the image
    pixList = list(pixList)
    for pix in pixList:
        # print(pix)
        # Intensity
        # Intensity = 0.299R + 0.587G + 0.114B
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
        # print(v1, v2, v3)
        # Converts to 6 digit binary, ensuring that the change isn't transparent from the value
        v1, v2, v3 = v1.rjust((8-len(v1)) + len(v1), '0')[:2], v2.rjust(
            (8-len(v2)) + len(v2), '0')[:2], v3.rjust((8-len(v3)) + len(v3), '0')[:2]
        six_digit_code = str(v1) + str(v2) + str(v3)
        # six_digit_code = v1[:2] + v2[:2] + v3[:2]
        # print(v1, v2, v3)
        # print(six_digit_code)
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
        # for i in range(len(target_bin)):
        #     distance += abs(((target_bin[i]) / (target_size)
        #                      ) - (image_bin[i] / (image_size)))
    # Handles Color Code values
    elif type == 'CC':
        # Gets the color code bin for the target image
        target_bin = session.get('imageList')[target]['bins'][1]
        image_bin = session.get('imageList')[image]['bins'][1]
        # Loops through all the binned proportions and calculates using Manhattan distance
    else:  # Error
        return -1
    for i in range(len(target_bin)):
        distance += abs(((target_bin[i]) / (target_size)
                         ) - (image_bin[i] / (image_size)))
    return distance


# Helper Functions for simplicity
def _convert_to_binary(num):
    return bin(num).replace("0b", "")
