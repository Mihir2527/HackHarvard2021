from django.db import models
from datetime import datetime
# Create your models here.
class HistoryData(models.Model):
    entry_id = models.BigAutoField(primary_key=True)
    uname=models.CharField(default="noname",max_length=20)
    infection=models.CharField(default="noinfection",max_length=300)
    start_date=models.DateField(default=datetime.now)
    end_date=models.DateField(default=datetime.now)
    medicine=models.CharField(default="nomedicine",max_length=300)
    outcome=models.CharField(default="neutral",max_length=20)
    
    # def  __str__(self):
    #     return self.entry_id