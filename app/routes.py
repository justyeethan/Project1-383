from app import app
import math
import random
import os
from flask import render_template, url_for, request, redirect, session
from collections import defaultdict
import numpy as np

# NOTE TESTING ONLY if you want to refresh your session constantly
app.secret_key = os.urandom(32)
np.set_printoptions(threshold=np.inf)


@app.route('/')
@app.route('/index')
def index():
    """The index page of the app.
    This page is the main page of the app. It is the first page the user sees when they visit the app.
    It will let you submit different genetic sequences and will return the results of the analysis based on the intensity of the radiation submitted.

    Returns:
        render_template (_type__): HTML template of the index page
    """
    return render_template('index.html', results=None)


@app.route('/parse', methods=['POST'])
def parseSequence():
    """
    Parses the sequence and returns the results of the analysis based on the intensity of the radiation submitted.

    Returns:
        template _type_: HTML file from templates folder
    """
    sequence = request.form.get('gene')
    l = ['C', 'A', 'G', 'T']
    intensity = request.form.get('intensity', 1.0)  # Intensity of Radiation
    genetic_sequence = sequence.upper()
    # Checks validity of sequence
    # if len(genetic_sequence) < 40:
    #     print('wrong beep')
    #     return render_template('index.html', error='Invalid Sequence length')
    for i in genetic_sequence:
        if i not in l:
            return render_template('index.html', error='Invalid Sequence')
    # Checks validity of intensity
    try:
        intensity = float(intensity)
        if 0 < intensity < 2:
            # Applies sequence to intensity
            res = mutation(genetic_sequence, intensity)
            print('beep')
            if res == genetic_sequence:
                return render_template('index.html', initial=sequence.upper(), results=genetic_sequence, error='No Mutation')
            return render_template('index.html', initial=sequence.upper(), results=genetic_sequence, error=None)
        else:
            print('wrong beep')
            return render_template('index.html', error='Invalid Intensity')
    except:
        print('wrong beep')
        return render_template('index.html', error='Invalid Intensity')


def mutation(sequence, intensity):
    """Mutation randomization and generation

    Args:
        sequence (string): The mutation sequence
        intensity (int): The strength of the mutation.
    """
    pos = random.randint(1, intensity)
    l = ['C', 'A', 'G', 'T']
    cdna = ''
    if pos > 50:
        changePos = random.randint(0, len(sequence)-1)
        dl = []
        dl[:0] = sequence
        ch = dl(changePos)
        l.remove(ch)
        cl = []
        cl[:0] = sequence
        cdna = ''.join([str(elem) for elem in cl])
    else:
        cdna = sequence
    print(cdna)
    return cdna
