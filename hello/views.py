from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Sentiment




def hello(request):
    table = Sentiment.object.all()
    context = [
        'table' : table
    ]
    return render(request, "home.html", context)

