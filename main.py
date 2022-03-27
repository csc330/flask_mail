# To run, do the following first:
# 1) install required modules:
#    sudo pip3 install flask-mail flask-bootstrap flask-moment
# 2) Set the values of the 3 variables in .flaskenv as follows:
#    MAIL_USERNAME=your_gmail_address
#    MAIL_PASSWORD=your_gmail_password
#    MAIL_SENDER_NAME=your_name
# 3) In the security settings of your Google account, create an app password,
#    which you will use in this app (not your account password)

from flask import Flask, render_template, flash
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
import os


class SendEmail(FlaskForm):
    email = StringField('Recipient: ', validators=[DataRequired()])
    message = TextAreaField('Your message:', validators=[DataRequired()])
    submit = SubmitField('Send')

app = Flask(__name__)
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_APP_PASSWORD = os.environ.get('MAIL_APP_PASSWORD')
MAIL_SENDER_NAME = os.environ.get('MAIL_SENDER_NAME')

app.config.update(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 465,
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True,
        MAIL_USERNAME = MAIL_USERNAME,
        MAIL_PASSWORD = MAIL_APP_PASSWORD,
        MAIL_DEFAULT_SENDER = (MAIL_SENDER_NAME, MAIL_USERNAME),
        SECRET_KEY = 'some secret key for CSRF')

mail = Mail(app)
moment = Moment(app)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def send_mail():
    mail_form = SendEmail()
    if mail_form.validate_on_submit():
        recipient = mail_form.email.data
        message = mail_form.message.data
        subject = 'Test Flask email'
        msg = Message(subject, recipients=[recipient], body = message)
        mail.send(msg)
        mail_form.email.data = ''
        mail_form.message.data = ''
    return render_template('index.html', form=mail_form)
