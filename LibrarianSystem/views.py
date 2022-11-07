from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from LibraryCatalog.forms import searchForm
from .forms import signupForm

# Create your views here.
def manageHome(request):
    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.is_staff:
        return HttpResponseForbidden('You are not authorized to access this resource')
    else:
        context = {
            'searchForm': searchForm(),
        }
        return render(request, 'manageHome.html', context=context)

def manageRegister(request):
    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.is_staff:
        return HttpResponseForbidden('You are not authorized to access this resource')
    else:
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
    
