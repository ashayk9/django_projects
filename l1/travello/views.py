from django.http import Http404
from django.shortcuts import render
from .models import Destination
import requests


# Create your views here.
def index(request):
    dest = Destination.objects.all()
    return render(request, 'index.html', {'dest': dest})


def individual_dest(request, primary_key):

    try:
        d = Destination.objects.get(id=primary_key)
    except Destination.DoesNotExist:
        raise Http404('Destination does not exist')

    return render(request, 'destination.html', {'d': d})











































