from django.contrib import admin
from django.urls import path,include
from History import views

urlpatterns = [
    path('',views.getHistoryPage,name="History"),
]
