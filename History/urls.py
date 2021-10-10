from django.contrib import admin
from django.urls import path,include
from History import views

urlpatterns = [
    path('',views.getHistoryPage,name="History"),
    path('newrecord/',views.newRecordPage,name="newRecord"),
    path('generateReport/',views.getReport,name="generateReport"),
    path('edit/<int:myid>',views.editView,name="Edit"),
    path('delete/<int:myid>',views.deleteView,name="Delete"),
]
