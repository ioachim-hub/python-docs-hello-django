from django.http import HttpResponse
from django.shortcuts import render
from .models import Sentiment

def hello(request):
    
    return render(request, "home.html")
