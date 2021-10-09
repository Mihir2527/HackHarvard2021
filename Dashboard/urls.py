from django.contrib import admin
from django.urls import path,include
from Dashboard import views


urlpatterns = [
    path('', views.getDashboardHomePage,name="Dashboard"),
]
