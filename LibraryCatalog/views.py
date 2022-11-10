from calendar import c
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.postgres import search
from .models import BookInstance, Author, Book, BookGenre
from .forms import searchForm
from django.contrib.auth.decorators import login_required        

# Create your views here.
def index(request):
    """View Function for Library Catalog Home Page"""
    

    num_availableBooks = BookInstance.objects.filter(status='a').count()
    num_authors = Author.objects.all().count()
    num_books = Book.objects.all().count()
    print(num_availableBooks)

    context = {
        'num_availableBooks' : num_availableBooks,
        'num_authors' : num_authors,
        'num_books' : num_books,
        'searchForm' : searchForm()
    }

    return render(request, 'index.html', context=context)


def book(request, pk):

    book = Book.objects.get(pk=pk)
    if(book is None):
        return HttpResponseNotFound('There aren\'t any books at this url!') 

    bookInstances = book.instances.all()
    for bookI in bookInstances:
        bookI.status = bookI.get_status_display() 

    context = {
        'bookTitle' : book.title,
        'bookAuthor' : book.author,
        'bookSummary' : book.summary,
        'bookGenre' : book.genre,
        'bookLanguage' : book.language,
        'bookInstances' : bookInstances
    }

    return render(request, 'bookView.html', context=context)



def account(request):
    pass
        


def search(request):
    
    tsearchForm = searchForm(request.GET)

    if tsearchForm.is_valid():
        bookTitle = tsearchForm.cleaned_data['searchParam']
    else:
        return HttpResponseNotFound('Invalid Search Query!')
    searchResults = Book.objects.filter(title__search=bookTitle)

    context = {
        'searchResults' : searchResults,
    }
    return render(request, 'searchResultView.html', context=context)


