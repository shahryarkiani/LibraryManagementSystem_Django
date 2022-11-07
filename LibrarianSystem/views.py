from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from LibraryCatalog.forms import searchForm
from .forms import signupForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

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
        userData.is_valid()
        print(userData.cleaned_data)
        return HttpResponse(userData)

    else:
        context = {
            'registerForm' : signupForm(),
        }
        return render(request, 'manageRegister.html', context=context)
    
