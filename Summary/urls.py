from django.contrib import admin
from django.urls import path,include
from Summary import views

urlpatterns = [
    path('',views.getHomePage,name="SummaryHome"),
    path('generateReport/',views.getReport,name="Report"),
]
