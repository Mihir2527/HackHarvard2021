from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User # The default User Table created by Django 
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout

# Create your views here.
def getHomePage(request):
    return render(request,"Basic/home.html")