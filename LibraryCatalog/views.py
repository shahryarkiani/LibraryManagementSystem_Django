from django.http import HttpResponseNotFound
from django.shortcuts import render

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
    for bookI in bookInstances:
        bookI.status = bookI.get_status_display()

    context = {
        'book': book,
        'bookInstances': bookInstances,
        'searchForm': searchForm()
    }

    return render(request, 'bookView.html', context=context)


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