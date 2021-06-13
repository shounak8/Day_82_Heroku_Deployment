from flask import Flask, render_template, redirect, url_for, flash, abort, request, send_from_directory
from flask_bootstrap import Bootstrap
from forms import SentimentAnalysisInput, SentimentAnalysisOutput
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length
import smtplib
import os
from boto.s3.connection import S3Connection

# s3 = S3Connection(os.environ['FLASK_SECRET_KEY'], os.environ['SHOUNAK_EMAIL'],
#                   os.environ['SHOUNAK_EMAIL_PASSWORD'], os.environ['COMPANY_EMAIL'])


#FLASK_SECRET_KEY="hello"
app = Flask(__name__)
#Credentials
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
SHOUNAK_EMAIL = os.environ.get("SHOUNAK_EMAIL")
SHOUNAK_EMAIL_PASSWORD = os.environ.get("SHOUNAK_EMAIL_PASSWORD")
COMPANY_EMAIL = os.environ.get("COMPANY_EMAIL")
Bootstrap(app)


import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

def sent_analyser(sentence):
    score = sid.polarity_scores(sentence)['compound']
    if score > 0.34:
        return ['👍','Positive Sentiment']
    elif score < -0.35:
        return ['👎','Negative Sentiment']
    else:
        return ['✊','Neutral Sentiment']


print(environ.get("SHOUNAK_EMAIL"))

def send_email(name, email, phone, message):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(SHOUNAK_EMAIL, SHOUNAK_EMAIL_PASSWORD)
        connection.sendmail(SHOUNAK_EMAIL,
                            COMPANY_EMAIL,
                            f"Subject: Website Contact mail from {name}\n\nDetails are as below:\n\nName:{name} \n"
                            f"Email:{email} \nPhone:{phone} \nMessage:{message}")
        connection.sendmail(SHOUNAK_EMAIL,
                            f"{email}",
                            f"Subject: Response submitted successfully\n\nHi {name} !!\n"
                            f"Thank you for visiting Indomitable Tech. We have received your response.\nDetails are as below:\n\nName:{name}\n"
                            f"Email:{email} \nPhone:{phone} \nMessage:{message}\n\nWe will get back to you soon\n\n"
                            f"Thanks and Regards,\n(On behalf of Indomitable Tech)\nShounak Deshpande\n9970536215")




@app.route("/")
def home():
    return render_template('index.html')



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():

    return render_template("contact.html")

@app.route("/form_submit", methods=["POST"])
def form_submit():
    responder_name = request.form["responder_name"]
    responder_email = request.form["responder_email"]
    try:
        responder_phone = request.form["responder_phone"]
    except:
        responder_phone = 'No phone number submitted'
    responder_message = request.form["responder_message"]

    send_email(name=responder_name, email=responder_email, phone=responder_phone, message=responder_message)
    return render_template("submit_response.html")


@app.route("/sentiment", methods=["POST","GET"])
def sentiment():
    sentiment_analysis_input = SentimentAnalysisInput()
    sentiment_analysis_output = SentimentAnalysisOutput()
    if sentiment_analysis_input.validate_on_submit():
        text = sentiment_analysis_input.sentiment.data
        result = sent_analyser(text)
        return_text = result[1]
        print(return_text)
        sentiment_analysis_output = SentimentAnalysisOutput(sentiment_output=return_text)
        return render_template("sentiment.html",
                               sentiment_analysis_input=sentiment_analysis_input,
                               sentiment_analysis_output=sentiment_analysis_output,
                               result = result)
    result = [None, None]
    return render_template("sentiment.html",
                           sentiment_analysis_input = sentiment_analysis_input,
                           sentiment_analysis_output = sentiment_analysis_output,
                           result = result)

@app.route('/download/file')
def download():
    return send_from_directory(directory='static',
                               path="files/Shounak_Deshpande_Resume_IT.pdf",
                               as_attachment=False)

if __name__=='__main__':
    app.run(debug=True)
