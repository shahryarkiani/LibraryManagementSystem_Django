from django.contrib import admin
from .models import Author, Book, BookGenre, BookInstance


# Register your models here.

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pk')

    inlines = [BookInstanceInline]

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')
    
    inlines = [BookInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_date')
    list_display = ('book', 'status', 'due_date', 'isbn', 'labelId')

admin.site.register(BookGenre)

