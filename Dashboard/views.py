from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def getDashboardHomePage(request):
    return render(request,"Dashboard/index.html")