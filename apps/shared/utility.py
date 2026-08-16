import re
import threading

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from twilio.rest import Client

from apps.accounts.models import VIA_PHONE_NUMBER, VIA_EMAIL, VIA_USERNAME

phone_pattern, email_pattern, username_pattern = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", r"^[a-z0-9_-]{5,50}$"

def check_auth_type(phone_number_or_email: str) -> str | None:
    if re.fullmatch(phone_pattern, phone_number_or_email):
        return VIA_PHONE_NUMBER
    elif re.fullmatch(email_pattern, phone_number_or_email):
        return VIA_EMAIL
    else:
        raise ValidationError('Invalid phone number or email format')

def check_login_type(user_input: str) -> str | None:
    if re.fullmatch(phone_pattern, user_input):
        return VIA_PHONE_NUMBER
    elif re.fullmatch(email_pattern, user_input):
        return VIA_EMAIL
    elif re.fullmatch(username_pattern, user_input):
        return VIA_USERNAME
    else:
        raise ValidationError('Invalid phone number or email format')

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Email:
    @classmethod
    def send_email(cls, data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=data['from_email'],
            to=data['to'],
        )
        if data.get('content_type') == 'html':
            email.content_subtype = 'html'
        EmailThread(email).start()

def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {'code': code}
    )
    Email.send_email(
        {
            'subject': 'Activate your account',
            'to': [email],
            'body': html_content,
            'from_email': 'rahimovilhomjon25@gmail.com',
            'content_type': 'html',
        }
    )

class SMSThread(threading.Thread):

    def __init__(self, phone_number, code):
        self.phone_number = phone_number
        self.code = code
        super().__init__()

    def run(self):
        send_phone_number(
            self.phone_number,
            self.code
        )

def send_phone_number(phone_number, code):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"You confirmation code: {code}\n",
        from_=settings.TWILIO_NUMBER,
        to=phone_number,
    )