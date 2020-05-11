from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('book_list', views.book_list_view, name='book_list_view'),
    path('book_list/<id>', views.book_detail_view, name='book_detail_view'),
    path('mybooks',views.loaned_books_by_user_list_view,name='user_book_list'),
    path('book_list/<id>/borrow', views.loan_book, name='loan_book'),
    path('author_list',views.author_list_view,name='author_list'),
    path('author_list/<author_id>', views.books_of_author_view, name='books_of_author'),
    path('book_list/<id>/return',views.return_book,name='return_book'),
    path('book_list/<id>/renew',views.renew, name='renew_book'),
    path('book_list/<id>/reserve',views.reserve, name='reserve_book'),
    path('book_list/<id>/unreserve',views.unreserve,name='unreserve_book'),
    #path('fine',views.fine,name='fine'),
]