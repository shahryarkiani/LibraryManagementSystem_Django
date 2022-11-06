from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from LibraryCatalog.forms import searchForm

# Create your views here.
def manageHome(request):
    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.is_staff:
        return HttpResponseForbidden('You are not authorized to access this resource')
    else:
        context = {
            'searchForm': searchForm()
        }
        return render(request, 'manageHome.html', context=context)
    
