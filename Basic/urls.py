from django.contrib import admin
from django.urls import path,include
from Basic import views

urlpatterns = [
    path('',views.getHomePage,name="Home"),
    path('login/',views.LoginAuthView.as_view(),name="Login"),
    path('register/',views.RegisterAuthView.as_view(),name="Register"),
    path('logout/',views.LogoutAuthView.as_view(),name="Logout"),
]
