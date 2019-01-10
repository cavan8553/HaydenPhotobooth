############ CAVAN MCLELLAN ############
#~~~~~~~~~~~~~~~18/12/18~~~~~~~~~~~~~~~#
########################################
# Server hosts a website that tweets   #
# a user input to Donald Trump         #
########################################

# importing specific classes from flask to optimize
import os
from flask import Flask, request, render_template, redirect
import cloudinary.uploader # website to host images for IFTTT
import requests
from werkzeug.utils import secure_filename

# declaring app variable as flask object
app = Flask(__name__)

UPLOAD_FOLDER = './temp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

APIkey = "173858322258362"
APIsecret = "pMAjaKswWS9oada_dN1wY0sZCm4"

# variables and the such
isLocked = False
url = 'https://maker.ifttt.com/trigger/Tweetmytweet/with/key/jNXrnP7IGnwBGQ1zG7JfoCdQFeejijhb3ptdUHLOPG6'
tweettext = ""

global TweetJson


@app.route('/', methods=['GET', 'POST'])
def index():
    global isLocked
    global tweettext
    global imgurl

# upon submitting the form, the web page will try and tweet it via IFTTT, if it can't for whatever reason
# It'll just tell the user there was an error
    if request.method == 'POST':

        # ~~~~~~~ the following code works with cloudinary's API: ~~~~~~~~~

        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)

        # runs only if file received, reduces headache
        if file:

            # file name variable needed for future reference
            filename = secure_filename(file.filename)

            # everything gets put into the temp folder (reduces headache)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filelocation = './temp/' + str(filename)

            # cloudinary has it's own library to use as an alternative
            cloudinary.uploader.unsigned_upload(filelocation, 'derekc', cloud_name = 'cavan')
            imgurl = 'https://res.cloudinary.com/cavan/image/upload/v1547063215/' + str(filename)
            print("image available at: " + imgurl)

        # ~~~~~~~ the following code works with IFTTT's API: ~~~~~~~~~

        try:

            # sends IFTTT a JSON containing the text from the form as well as
            # the image url from cloudinary.
            tweettext = request.form.get('tweet')
            print(tweettext + " was tweeted")
            TweetJson = {"value1": tweettext, "value2": imgurl}
            requests.post(url, TweetJson)
            return render_template('sent.html')

        except:
            # sends a webpage back to the user instead of crashing (reduces headache)
            print("error")
            return render_template('Locked.html')

# if the user goes to the url, it will return the web page with the form
# simple stuff, really
    if request.method == 'GET':
        return render_template('index.html')


# run the server on port 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)
