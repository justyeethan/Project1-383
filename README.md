# Mutation Detection and visualizer | CSS 383

## Description
This is a simple mutation detection project for CSS 383, Bioinformatics. This can simulate the radiation dosage, and provide more information on how to treat the patient. This is a simple web application that uses Flask, and a few other libraries to run.
Here is documentation on setup and usage.

# Easy Viewing

It should take a few milliseconds at first to fetch all the images, but after that, it should cache the website and run normally depending on your internet connection.

## To Run the Flask app manually (MacOS/Linux)

1.  Open the base directory to this project in a \*NIX-based OS

2.  Load in a new python envrionment (Optional but best practice to mitigate conflicting deps) `python3 -m venv venv`

3.  Source the new virtual environment (Optional but best practice to mitigate conflicting deps) `source venv/bin/activate`

4.  Install requirements using `pip3 install -r requirements.txt`

5.  To run the app, use `flask run`  or  `python3 run.py`

6.  Make sure port 5000 is open

7.  Open the browser and navigate to the link provided in the terminal, should be http://127.0.0.1:5000/

8.  Wait for the application to load (it should take a few seconds, but after, it will cache all the images and their features to cookies, and it will run normally)

## Running the Flask app through setup.sh (MacOS/Linux)

1.  Open the base directory to this project in a \*NIX-based OS

2.  Make sure the file has executable permissions `chmod +x setup.sh`

3.  Make sure port 5000 is open

4.  Run the script `./setup.sh` or `bash setup.sh`

5.  Open the browser and navigate to the link provided in the terminal, should be http://127.0.0.1:5000/

6.  Wait for the application to load (it should take a few seconds, but after, it will cache all the images and their features to cookies, and it will run normally)

