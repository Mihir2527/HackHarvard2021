from django.http.response import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
def getDashboardHomePage(request):
    if request.user.is_anonymous:
        return redirect("/login")
        
    return render(request,"Dashboard/index.html")