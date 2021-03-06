from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from . forms import SignupForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout


def home(request):
    return render(request,'base.html',{})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.info(request, 'login successful')
                return redirect('item_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})


def register(request):
    if request.method =='POST':
        form = SignupForm(request.POST)
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

            return redirect('item_list')
        else:
            messages.info(request,'invalid username or password')
    else:
        form = SignupForm()

    return render(request, 'register.html', {'form':form})


def logout(request):
    auth.logout(request)
    return redirect('/')
