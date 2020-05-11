from django.shortcuts import render
from .forms import Contact_Form
from .models import Contact


def contactf(request):
    if request.method == 'POST':
        form = Contact_Form(request.POST)
        if form.is_valid():
            form.save()
            form = Contact_Form()

    else:
        form = Contact_Form()
    return render(request, 'contact.html', {'form': form})
