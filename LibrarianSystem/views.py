from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

from LibraryCatalog.models import BookInstance

from .forms import signupForm
from .utilfuncs import *

# Create your views here.


@staff_member_required
@login_required(login_url='/accounts')
def manageHome(request):
    return render(request, 'manageHome.html')


@staff_member_required
@login_required(login_url='/accounts')
def manageRegister(request):

    if request.method == 'POST':  # Staff is registering a new user
        userData = signupForm(request.POST)
        if userData.is_valid():
            cardNum = generateCardNumber()
            userData = userData.cleaned_data
            newUser = User.objects.create_user(username=cardNum, email=userData['email'],
                                               first_name=userData['first_name'], last_name=userData['last_name'], is_staff=False)
            context = {
                'newUser': newUser
            }
            sendCreatePasswordEmail(newUser)
            return render(request, 'manageRegisterSuccess.html', context=context)

    else:  # GET Request for the register page
        context = {
            'registerForm': signupForm(),
        }
        return render(request, 'manageRegister.html', context=context)


@staff_member_required
@login_required(login_url='/accounts')
def manageCheckout(request):
    if request.method == 'GET':
        return render(request, 'manageCheckout.html')
    #If the user is submitting a checkout
    elif request.method == 'POST':
        # Find User and store all labels being checked out
        user = User.objects.get(username=request.POST['id'])
        labelIds = request.POST.getlist('labelId')

        # Process Checkout for all the books and user
        books = processCheckout(labelIds=labelIds, checkoutUser=user)
        context = {
            'books': books,
            'userCheckout': user
        }

        # Serves success checkout page
        return render(request, 'successCheckout.html', context=context)


@staff_member_required
@login_required(login_url='/accounts')
def bookListView(request):
    #Used for htmx, returns html containing information about book 
    try:
        bookInstance = BookInstance.objects.get(labelId=request.GET['bookLabelId'])
        context = {
            'book': bookInstance.book,
            'bookInstance': bookInstance
        }
        return render(request, 'bookListView.html', context=context)
    except:
        return HttpResponse('')


@staff_member_required
@login_required(login_url='/accounts')
def userListView(request):
#This method is for use with htmx
#it returns html containing the user if they exist
    try:
        user = User.objects.get(username=request.GET['id'])
        context = {
            'user': user,
            'id': request.GET['id']
        }
        return render(request, 'userCheckoutView.html', context=context)
    except:
        return HttpResponse('')


@staff_member_required
@login_required(login_url='/accounts')
def manageUser(request):
    return render(request, 'manageUsers.html')


@staff_member_required
@login_required(login_url='/accounts')
def manageUserDetail(request, pk): 
    #This view returns a manage page for a specific user
    try:
        user = User.objects.get(username=str(pk))
        context = {
           'user': user,
           'books': user.borrowed.all()
        }
        return render(request, 'manageUserDetail.html', context)
    except User.DoesNotExist:
        return HttpResponseNotFound('This User does not exist')


@staff_member_required
@login_required(login_url='/accounts')
def searchUser(request):
    #This method returns a table of matching users with links to their pages
    name = request.GET.get('nameSearch')
    id = request.GET.get('cardNumber')

    users = []

    #If the search paramater includes a name
    if name:
        #search by full name
        users = User.objects.annotate(fullName=Concat('first_name', Value(' '), 'last_name')).filter(fullName__search=name)
        context = {'users': users}
        return render(request, 'userManageSearchView.html', context=context)
    elif id: #the search parameter includes an id
        try:
            print('here') 
            sUser = User.objects.get(username=id)
            users.append(sUser)
            return render(request, 'userManageSearchView.html', context={'users': users})
        except User.DoesNotExist:
            return HttpResponse('')
    else:
        return HttpResponse('')

@staff_member_required
@login_required(login_url='/accounts')
def manageHolds(request):
    requestedHolds = BookInstance.objects.filter(hold_status='r')
    context = {
        'holds': requestedHolds
    }
    return render(request, 'manageHold.html', context=context)

@staff_member_required
@login_required(login_url='/accounts')
def manageHoldsDetail(request, id):
    if request.method == 'GET':
        try:
            bookI = BookInstance.objects.get(labelId=id)
            context = {
                'book' : bookI
            }
            return render(request, 'manageHoldDetail.html', context=context)
        except BookInstance.DoesNotExist:
            return HttpResponseNotFound('There is no book associated with the specified label id')
    elif request.method == 'POST':
        requestedHolds = BookInstance.objects.filter(hold_status='r')
        context = {
            'holds': requestedHolds
        }
        return render(request, 'manageHold.html', context=context)
    pass