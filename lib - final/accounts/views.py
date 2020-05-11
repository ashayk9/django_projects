from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,logout,login
from django.shortcuts import redirect
from .forms import SignupForm
from django.contrib import messages,auth


def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST or None)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('user_book_list')
    else:
        form=AuthenticationForm()

    context={
        'form':form,
    }
    return render(request,'login.html',context=context)


def logout_view(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method=='POST':
        form2=SignupForm(request.POST)
        if form2.is_valid():
            user=form2.save()
            user.first_name=form2.cleaned_data.get('first_name')
            user.last_name = form2.cleaned_data.get('last_name')
            user.email = form2.cleaned_data.get('email')
            user.username=form2.cleaned_data.get('username')
            user.password1=form2.cleaned_data.get('password1')
            user.password2=form2.cleaned_data.get('password2')
            user.save()
            messages.info(request,"user created")


            user=authenticate(username=user.username,password=user.password1)
            auth.login(request,user)
            return redirect('/')

        else:
            messages.info(request,"incorrect username or password")
    else:
        form2=SignupForm()

    context={
            'form2':form2,
    }
    return render(request,'register.html',context=context)