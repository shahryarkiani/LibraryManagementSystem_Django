from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import get_template
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from random import randint
from django.contrib.auth.models import User


def generateCardNumber():
    rand = randint(1_000_000_00, 9_999_999_99)
    while(User.objects.filter(pk=str(rand)).exists()):
        rand = randint(1_000_000_00, 9_999_999_99)
    return str(rand)

def sendCreatePasswordEmail(user):
    subject = "Setup Your Library Card Password"
    toMail = user.email
    context = {
		'domain':'127.0.0.1:8000',
		'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
		'user': user,
		'token': default_token_generator.make_token(user),
		'protocol': 'http',
	}
    message = get_template('register_email.html').render(context)
    
    send_mail(
        subject,
        message,
        from_email='Test@mail.com',
        recipient_list=[toMail]
    )

def sendReceiptEmail(user):
    subject = "Library Checkout Receipt"
    toMail = user.email
    message = get_template('checkout_email.html').render()