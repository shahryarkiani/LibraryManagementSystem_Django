from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from random import randint
from django.shortcuts import render
from django.contrib.auth.models import User
from LibraryCatalog.forms import searchForm
from .forms import signupForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

# Create your views here.

@staff_member_required
@login_required(login_url='/accounts')
def manageHome(request):
    context = {
        'searchForm': searchForm(),
    }
    return render(request, 'manageHome.html', context=context)

@staff_member_required
@login_required(login_url='/accounts')
def manageRegister(request):
    
    if request.method == 'POST':
        userData = signupForm(request.POST)
        if userData.is_valid():
            cardNum = generateCardNumber()
            userData = userData.cleaned_data
            firstName = userData['first_name']
            lastName = userData['last_name']
            email = userData['email']
            newUser = User.objects.create_user(username=cardNum, email=email, first_name=firstName, last_name=lastName, is_staff=False)
            context = {
                'newUser' : newUser
            }
            #newUser.delete()
            sendCreatePasswordEmail(newUser)
            return render(request, 'manageRegisterSuccess.html', context=context)

    else:
        context = {
            'registerForm' : signupForm(),
        }
        return render(request, 'manageRegister.html', context=context)
    
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