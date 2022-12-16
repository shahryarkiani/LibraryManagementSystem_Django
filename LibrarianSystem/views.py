from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import HttpResponse
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

        sendReceiptEmail(user, books)

        # Serves success checkout page
        return render(request, 'successCheckout.html', context=context)


@staff_member_required
@login_required(login_url='/accounts')
def bookListView(request):

    bookInstance = BookInstance.objects.get(labelId=request.GET['bookLabelId'])

    if not bookInstance == None:
        context = {
            'book': bookInstance.book,
            'bookInstance': bookInstance
        }
        return render(request, 'bookListView.html', context=context)
    else:
        return HttpResponse('')


@staff_member_required
@login_required(login_url='/accounts')
def userListView(request):
    user = User.objects.get(username=request.GET['id'])

    if not user == None:
        context = {
            'user': user,
            'id': request.GET['id']
        }
        return render(request, 'userCheckoutView.html', context=context)
    else:
        return HttpResponse('')


@staff_member_required
@login_required(login_url='/accounts')
def manageUser(request):
    return render(request, 'manageUsers.html')


@staff_member_required
@login_required(login_url='/accounts')
def manageUserDetail(request, user):
    # TODO returns management view of a specific user
    pass


@staff_member_required
@login_required(login_url='/accounts')
def searchUser(request):
    name = request.GET.get('name')
    id = request.GET.get('id')
    if name:
        users = User.objects.annotate(full_name=Concat(
            "first_name", Value(" "), "last_name")).filter()
        context = {'users': users}
        return render(request, 'userManageSearchView', context=context)
    elif id:
        sUser = User.objects.get(username=id)
        if not sUser == None:
            return manageUserDetail(request, sUser)
        else:
            return HttpResponse('')
    else:
        return HttpResponse('')
