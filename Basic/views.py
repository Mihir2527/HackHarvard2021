from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib import messages
from django.views import View


# Create your views here.
def getHomePage(request):
    return render(request,"Basic/home.html")

class LoginAuthView(View):
    
    template_name='Basic/login.html'
    
    def get(self,request):
        print("inside get route of user login")
        return render(request,self.template_name)

    def post(self,request):
        print("inside post route of user login")
        u=request.POST.get('username')
        p=request.POST.get('password')

        user = authenticate(username=u, password=p)
        if user is not None:
            # A backend authenticated the credentials
            login(request,user)

            messages.success(request, 'Successfully logged in!!')
            return redirect("/dashboard")
        else:
            # No backend authenticated the credentials
            messages.error(request, 'Invalid Login Credentials!!')
            return render(request,self.template_name)

class RegisterAuthView(View):

    template_name='Basic/register.html'
    
    def get(self,request):
        print("inside get route of user registration")
        return render(request,self.template_name)

    def post(self,request):
        # add credentials to database
        print("inside post route of user registration")
        u=request.POST.get('username')
        e=request.POST.get('email')
        p1=request.POST.get('pass1')
        p2=request.POST.get('pass2')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')

        global err_flag
        err_flag=0
        
        if User.objects.filter(username=u).exists():
            messages.error(request,'This username is already taken!!')
            err_flag=1

        if(len(u)>10):
            
            messages.error(request,'Username should be less than 10 characters!!')
            err_flag=1
        
        if not u.isalnum():
            messages.error(request,'Username should contain only letters and numbers!!')
            err_flag=1

        if(p1!=p2):
            messages.error(request, 'Passwords do not match!!')
            err_flag=1
        
        if(err_flag==1):
            return render(request,self.template_name)

        myUser=User.objects.create_user(u,e,p1)
        myUser.first_name=fname
        myUser.last_name=lname
        messages.success(request, 'Your profile has been created successfully!!')
        
        myUser.save()

        return redirect("/dashboard") 

class LogoutAuthView(View):

    def get(self,request):
        print("inside logout post route")
        logout(request)
        return redirect('/login')