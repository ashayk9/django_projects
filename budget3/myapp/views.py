from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, ExpensesForm
from django.views import generic
from .models import Profile, ExpenseInfo
from django.shortcuts import  get_object_or_404


def home(request):
    return render(request, 'base.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.info(request, 'login successful')

                return redirect('details', user)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.dob = form.cleaned_data.get('dob')

            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth.login(request, user)

            return redirect('create',user=request.user)
        else:
            messages.info(request, 'invalid username or password')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    auth.logout(request)
    return redirect('/')


def create(request, user):
    obj = get_object_or_404(Profile, user=request.user)
    new_obj=None
    if request.method=='POST':
        form = ExpensesForm(request.POST or None)
        if form.is_valid():

            expenditure = form.cleaned_data.get('expenditure')
            intake = form.cleaned_data.get('intake')
            date_added = form.cleaned_data.get('date_added')
            print(form.cleaned_data)

            new_obj=ExpenseInfo.objects.get_or_create(
                user=request.user,
                expenditure=expenditure,
                intake=intake,
                date_added=date_added,

            )

    form=ExpensesForm()

    context={
        'obj': obj,
        'form':form,
        'new_obj':new_obj
             }
    return render(request, 'index.html',context=context)


def details(request, user):
    #obj1 = get_object_or_404(Profile, id=id)
    #obj2 = get_object_or_404(ExpenseInfo,id=id)
    obj1 = Profile.objects.get(user=request.user.id)
    obj2 = ExpenseInfo.objects.get(user=request.user.id)

    context={
            'obj1':obj1,
            'obj2':obj2,
    }
    return render(request,'details.html',context=context)


# class Details(generic.DetailView, LoginRequiredMixin):
#     model = Profile
#     context_object_name = 'd'
#     template_name = 'index.html'
#     login_url = 'login'
#     redirect_field_name = 'details'


# def expense(request, pk):
#     obj=ExpenseInfo.objects.get(id=pk)
#     if request.method == 'POST':
#         form2 = ExpensesForm(request.POST)
#         if form2.is_valid():
#             user = form2.save()
#             user.refresh_from_db()
#             user.expenses.intake = form2.cleaned_data.get('intake')
#             user.expenses.expenditure = form2.cleaned_data.get('expenditure')
#             user.expenses.date_added = form2.cleaned_data.get('date_added')
#
#             user.save()
#
#             # username = form.cleaned_data.get('username')
#             # password = form.cleaned_data.get('password1')
#             # user = authenticate(username=username, password=password)
#             # auth.login(request, user)
#             return redirect('details', user.id)
#         else:
#             messages.info(request, 'invalid input')
#
#     form2 = ExpensesForm()
#     print(obj)
#     context={
#         'form2': form2,
#         'obj':obj
#     }
#
#     return render(request, 'exp.html',context=context )
