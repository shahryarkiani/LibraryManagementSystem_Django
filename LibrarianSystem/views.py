from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from LibraryCatalog.forms import searchForm
from .forms import signupForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .utilfuncs import generateCardNumber, sendCreatePasswordEmail, sendReceiptEmail
from LibraryCatalog.models import BookInstance

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

@staff_member_required
@login_required(login_url='/accounts')
def manageCheckout(request):
    if request.method == 'GET':
        return render(request, 'manageCheckout.html')
    elif request.method == 'POST':
        #Send Success Page, Send Receipt Email to User
        return redirect()

def bookListView(request):
    
    bookInstance = BookInstance.objects.filter(isbn=request.GET['isbn']).first()

    if not bookInstance == None:
        context = {
            'book' : bookInstance.book,
            'bookInstance' : bookInstance
        }
        return render(request, 'bookListView.html', context=context)
    else:
        return ""

def userListView(request):
    
    user = User.objects.filter(username=request.GET['id'])

    if not user == None:
        context = {
            'user' : user
        }
        return render(request, 'userListView.html', context=context)
    else:
        return ""
    

