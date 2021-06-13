from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField

##WTForm


class SentimentAnalysisInput(FlaskForm):
    sentiment = CKEditorField("Sentiment", validators=[DataRequired()])
    submit = SubmitField("Analyse")

class SentimentAnalysisOutput(FlaskForm):
    sentiment_output = StringField("Analysis")
