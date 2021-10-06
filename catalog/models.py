from django.db import models
from django.urls import reverse
import uuid

from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    """
    Жанр книг.

    """
    name = models.CharField(max_length=100, help_text='Enter genre of book you searching')

    def __str__(self):

        return self.name


class Book(models.Model):
    
    title = models.CharField(max_length=200)

    """ В поле автор мы используем от одного к множеству(foreign key) """    
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.CharField(max_length=1000, help_text='Аннотация к книги')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField('Genre', help_text='Выберете жанр книги')

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'


class BookInstanse(models.Model):
    """ Модель представляет специфическую копию книги, которую можно взять в библиотеке """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Id книги')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    ) 

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность книги')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)

    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)


class Lang(models.Model):
    """ Язык книги """
    name = models.CharField(max_length=200, help_text='Lang of the book')

    def __str__(self) -> str:
        return self.name
