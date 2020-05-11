from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def hello(request):
    return render(request, 'hello.html', {})


def add(request):
    val1 = int(request.POST['num1'])
    val2 = int(request.POST['num2'])
    result = val1 + val2

    return render(request, 'result.html', {'result': result})
