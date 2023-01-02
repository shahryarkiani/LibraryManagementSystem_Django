from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from .forms import searchForm
from .models import Author, Book, BookInstance

# Create your views here.


def index(request):
    """View Function for Library Catalog Home Page"""
    num_availableBooks = BookInstance.objects.filter(status='a').count()
    num_authors = Author.objects.all().count()
    num_books = Book.objects.all().count()
    print(num_availableBooks)

    context = {
        'num_availableBooks': num_availableBooks,
        'num_authors': num_authors,
        'num_books': num_books,
        'searchForm': searchForm()
    }

    return render(request, 'index.html', context=context)


def book(request, pk):
    #Returns view for a specific book
    #Includes all instances of books and current availibility
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return HttpResponseNotFound('There aren\'t any books at this url!')

    bookInstances = book.instances.all()

    context = {
        'book': book,
        'bookInstances': bookInstances,
        'searchForm': searchForm()
    }

    return render(request, 'bookView.html', context=context)

@login_required(login_url="/accounts")
def account(request):
    #Returns account view for user, containg all their holds and borrowed books
    context = {
        'books': request.user.borrowed.all(),
        'holds': request.user.holds.all(),
        'searchForm': searchForm()
    }

    return render(request, 'accountView.html', context=context)



def search(request):

    tsearchForm = searchForm(request.GET)

    if tsearchForm.is_valid():
        bookTitle = tsearchForm.cleaned_data['searchParam']
    else:
        return HttpResponseNotFound('Invalid Search Query!')
    searchResults = Book.objects.filter(title__search=bookTitle)

    context = {
        'searchResults': searchResults,
        'searchForm': searchForm()
    }
    return render(request, 'searchResultView.html', context=context)

def explore(request):
    books = Book.objects.all()
    bookPaginator = Paginator(books, 5)

    pageNum = request.GET.get('page')
    bookList = bookPaginator.get_page(pageNum)
    context = {
        'searchForm': searchForm(),
        'books' : bookList
    }
    return render(request, 'exploreView.html', context=context)


@login_required(login_url="/accounts")
def requestHold(request, id):
    if request.method == 'GET':
        try:
            book = BookInstance.objects.get(labelId=id)
            context = {
                'book' : book,
                'searchForm' : searchForm()
            }
            return render(request, 'requestHold.html', context=context)
        except BookInstance.DoesNotExist:
            return HttpResponseNotFound('This book does not exist')
    elif request.method == 'POST':
        try:
            book = BookInstance.objects.get(labelId=id)

            if 'submit_yes' in request.POST:
                #Marks book on hold for user
                if book.holder != None:
                    return HttpResponseBadRequest('Sorry, this book is already on hold for someone else')
                book.holder = request.user
                book.hold_status = 'r'
                book.save()
            elif 'cancel_yes' in request.POST:
                #Cancels hold for book
                if book.holder != request.user:
                    return HttpResponseBadRequest('Sorry, this book is on hold for someone else')
                book.holder = None
                book.hold_status = 'n'
                book.save()
            #Redirects user to their account view, where they can confirm the book was put on hold
            return redirect('account-view')

        except BookInstance.DoesNotExist:
            return HttpResponseNotFound('This book does not exist')
