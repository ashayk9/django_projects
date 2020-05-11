from django.shortcuts import render
from django.http import HttpResponse
from .forms import RawForm
from .models import Product


# Create your views here.
def index(request):
    return render(request, 'base.html', {})


def product_form(request):
    context = {}
    return render(request, 'rawform.html', context)
