from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
def getDashboardHomePage(request):
    if request.user.is_anonymous:
        return redirect("/login")

    user=User.objects.get(username=request.user)

    context={
        'name':user.first_name,
    }
        
    return render(request,"Dashboard/index.html",context)