import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class BookGenre(models.Model):
    """Model that represents a book genre"""
    genre_name = models.CharField(
        max_length=200, help_text='Enter a book genre')

    def __str__(self):
        """String that represents a Genre object"""
        return self.genre_name


class Author(models.Model):
    first_name = models.CharField(
        max_length=100, help_text='Enter the First Name of the Author')
    last_name = models.CharField(
        max_length=100, help_text='Enter the Last Name of the Author')
    date_of_birth = models.DateField(
        null=True, blank=True, help_text='Enter the Author\'s date of birth')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-view', args=[str(self.id)])

    def __str__(self):
        """String that represents an Author object"""
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey(Author, on_delete=models.PROTECT, null=True)

    summary = models.TextField(max_length=1000)

    genre = models.ManyToManyField(BookGenre)

    LANGUAGE = (
        ('e', 'ENGLISH'),
        ('s', 'SPANISH'),
        ('o', 'OTHER')
    )

    language = models.CharField(max_length=1, choices=LANGUAGE, blank=True,
                                default='u', help_text='Language the book is written in')

    def __str__(self):
        """String that represents a Book object"""
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        """Returns the URL that access data of a Book object"""
        return reverse('book-view', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a physical copy of a Book"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    isbn = models.CharField('ISBN', max_length=13)
    book = models.ForeignKey(
        Book, on_delete=models.RESTRICT, null=True, related_name="instances")
    due_date = models.DateField(null=True, blank=True)

    labelId = models.CharField(max_length=13, unique=True)

    LOAN_STATUS = (
        ('o', 'ON LOAN'),
        ('h', 'ON HOLD'),
        ('a', 'AVAILABLE'),
        ('u', 'UNAVAILABLE'),
    )

    HOLD_STATUS = (
        ('n', 'NO HOLDS'),
        ('r', 'HOLD REQUESTED'),
        ('h', 'ON HOLD - READY FOR PICKUP'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='a', help_text='Current Book Status')
    hold_status = models.CharField(
        max_length=1, choices=HOLD_STATUS, blank=True, default='n')

    holder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='holds')

    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrowed')

    def is_overdue(self):
        """Determines whether book is overdue"""
        return self.due_date and date.today > self.due_date

    class Meta:
        ordering = ['due_date']
        indexes = [
            models.Index(fields=['labelId'])
        ]

    def __str__(self):
        """String that represents a BookInstance object"""
        return f'{ ({self.book.title})}'
