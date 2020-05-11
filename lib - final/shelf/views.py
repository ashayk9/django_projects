from django.http import Http404
from django.shortcuts import render,redirect
from django.views import generic
from .forms import Loan_Form,Renew_form,Reserve_Form
from .models import Book, Author, Genre, BookInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import date


def home(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.count()

    # num_instances = BookInstance.objects.all().count()
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        # 'num_instances': num_instances,
        # 'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        # 'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def book_list_view(request):
    book_list = Book.objects.all()
    context = {'book_list': book_list}
    return render(request, 'book_list.html', context=context)


def book_detail_view(request, id):
    try:
        book_detail = Book.objects.get(id=id)
        # book_detail_instance=BookInstance.objects.filter(book=book_detail)
        # book_detail_instance_qs=book_detail_instance.first()
        # if book_detail_instance_qs is not None:
        #     if book_detail_instance_qs.is_overdue:
        #         print(date.today())
        #         print(book_detail_instance_qs.due_back)
        #         extra_days=date.today()-book_detail_instance_qs.due_back
        #         print(extra_days.days)
        #         book_detail_instance_qs.fine=extra_days.days*100
        #         print(book_detail_instance_qs.fine)





        #print(book_detail_instance_qs.borrower)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')
    context = {
        'book_detail': book_detail,
        #'book_detail_instance':book_detail_instance,
    }

    return render(request, 'book_detail.html', context=context)


# class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
#     """Generic class-based view listing books on loan to current user."""
#     context_object_name = 'bookinstance_list'
#     #model = BookInstance
#     template_name = 'userlist_view.html'
#     #paginate_by = 10
#
#
#     def get_queryset(self):
#         return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

#
@login_required
def loaned_books_by_user_list_view(request):
    user_book_list = BookInstance.objects.filter(borrower=request.user)
    user_reserve_book_list = BookInstance.objects.filter(reserver=request.user)

    context = {
        'user_book_list': user_book_list,
        'user_reserve_book_list':user_reserve_book_list,
    }

    return render(request, 'userlist_view.html', context=context)

@login_required
def loan_book(request, id):
    #obj = Book.objects.get(id=id)
    try:
        obj2=BookInstance.objects.get(id=id)

    except:
        obj2=None
    print(obj2)
    if request.method == 'POST':
        form = Loan_Form(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            due_back = form.cleaned_data.get('due_back')
            obj2.borrower=request.user
            obj2.due_back=due_back
            obj2.status='o'
            obj2.id=id
            obj2.save()

            return redirect('user_book_list')
    else:
        form = Loan_Form()
    context = {
        #'obj': obj,
        'obj2': obj2,
        'form': form,
    }
    return render(request, 'borrow.html', context=context)


def author_list_view(request):
    author_list = Author.objects.all()
    context = {'author_list': author_list}
    return render(request, 'author_list.html', context=context)


def books_of_author_view(request, author_id):
    author = Author.objects.get(author_id=author_id)
    books_of_author = Book.objects.filter(author=author)
    #books_of_author_qs = books_of_author.first()
    context = {
        'author': author,
        'books_of_author': books_of_author,
        #'books_of_author_qs': books_of_author_qs,
    }
    return render(request, 'books_of_author.html', context=context)

@login_required
def return_book(request, id):
    to_be_returned_book=BookInstance.objects.get(id=id)
    print(to_be_returned_book)

    if request.method == "POST":
        to_be_returned_book.status='a'
        to_be_returned_book.fine=0
        to_be_returned_book.due_back=None
        to_be_returned_book.borrower=None
        to_be_returned_book.save()
        context = {
            'to_be_returned_book': to_be_returned_book,
        }
        return redirect('user_book_list')
    else:
        book_detail_instance=BookInstance.objects.get(id=id)
        if book_detail_instance is not None:
            if book_detail_instance.is_overdue:
                print(date.today())
                print(book_detail_instance.due_back)
                extra_days=date.today()-book_detail_instance.due_back
                print(extra_days.days)
                book_detail_instance.fine=extra_days.days*100
                print(book_detail_instance.fine)
                context = {
                    'to_be_returned_book': to_be_returned_book,
                    'book_detail_instance':book_detail_instance,

                }
    return render(request,'return.html',context=context)


def renew(request, id):
    # book = Book.objects.get(id=id)
    # book_instance = BookInstance.objects.get(book=book)
    book_instance = BookInstance.objects.get(id=id)

    # print(book_inst)
    if book_instance.reservations != 'r':
        if request.method == 'POST':
            form = Renew_form(request.POST)
            if form.is_valid():
                book_instance.due_back = form.cleaned_data['renewal_date']
                book_instance.save()
                return redirect('user_book_list')
        else:
            form = Renew_form()
        context = {
            'form': form,
            'book_instance': book_instance,
        }
    else:
        print("cannot renew already reserved")
        context = {
            'book_instance':book_instance,
        }
    return render(request,'renew.html',context=context)


def reserve(request, id):
    book_instance = BookInstance.objects.get(id=id)
    if request.method == "POST":
        form=Reserve_Form(request.POST)
        if form.is_valid():
            book_instance.reservations = form.cleaned_data['reservations']
            book_instance.reserver = request.user
            book_instance.save()
    else:
        form=Reserve_Form()

    context={
        'form':form,
        'book_instance':book_instance,
    }

    return render(request,'reserve.html',context=context)

def unreserve(request, id):
    book_instance = BookInstance.objects.get(id=id)
    if request.method=="POST":
        book_instance.reservations = 'n'
        book_instance.reserver=None
        book_instance.save()
        return redirect('user_book_list')
    context={
            'book_instance':book_instance,
    }
    return render(request,'unreserve.html',context=context)



