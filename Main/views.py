from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def getHomePage(request):
    return HttpResponse("Home Page baby!")