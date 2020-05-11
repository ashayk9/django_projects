from django.db import models
from django.urls import reverse
import uuid  # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    no_of_books=models.IntegerField()
    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default='a',
    )
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        # Returns the url to access a detail record for this book.
        return reverse('book_detail_view', args=[str(self.id)])



class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    borrower=models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='borrower')
    book=models.ForeignKey(Book, on_delete=models.SET_NULL,null=True)
    due_back=models.DateField(null=True,blank=True)
    fine=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    reserver=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name='reserver')
    RESERVATION_STATUS =(
        ('r', 'Reserved'),
        ('n', 'Not Reserved'),
    )
    reservations=models.CharField(
        max_length=1,
        choices=RESERVATION_STATUS,
        default='n',
    )

    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
    )
    status=models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default='a',
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return self.book.title

    # def __str__(self):
    #     return f'{self.id} ({self.book.title})'

    def get_absolute_url(self):
        return reverse('book_loan_view', args=[str(self.id)])

    def get_absolute_url_for_return(self):
        return reverse('return_book', args=[str(self.id)])

    def get_absolute_url_for_renewal(self):
        return reverse('renew_book', args=[str(self.id)])

    def get_absolute_url_for_reserve(self):
        return reverse('reserve_book', args=[str(self.id)])

    def get_absolute_url_for_unreserve(self):
        return reverse('unreserve_book', args=[str(self.id)])

    # def get_absolute_url_for_fine(self):
    #     return reverse('fine', args=[str(self.id)])




# class BookInstance(models.Model):
#     borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4,
#                           help_text='Unique ID for this particular book across whole library')
#     book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
#     imprint = models.CharField(max_length=200)
#     due_back = models.DateField(null=True, blank=True)
#
#     @property
#     def is_overdue(self):
#         if self.due_back and date.today() > self.due_back:
#             return True
#         return False
#
#     LOAN_STATUS = (
#         ('m', 'Maintenance'),
#         ('o', 'On loan'),
#         ('a', 'Available'),
#         ('r', 'Reserved'),
#     )
#
#     status = models.CharField(
#         max_length=1,
#         choices=LOAN_STATUS,
#         blank=True,
#         default='m',
#         help_text='Book availability',
#     )
#
#     class Meta:
#         ordering = ['due_back']
#
#     def __str__(self):
#         return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
#    books = models.ForeignKey(Book,on_delete=models.CASCADE)
    author_id=models.IntegerField()

    class Meta:
        ordering = ['first_name','last_name']

    # def get_absolute_url(self):
    #     return reverse('books_of_author', args=[str(self.id)])
    def get_absolute_url(self):
        return reverse('books_of_author',args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


