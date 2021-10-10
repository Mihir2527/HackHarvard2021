from django.shortcuts import redirect, render
from History.models import HistoryData
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date

from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
def getHomePage(request):
    allUserHistory=HistoryData.objects.all()

    user=User.objects.get(username=request.user)
    name=user.username
    print("Username is: ",name)
    currUserHistory=allUserHistory.filter(uname=name)
    print("User history is: ",currUserHistory)


    # if not allUserHistory:
    #     print("empty")
    #     return render(request,"History/index.html")
    # else:
    #     print("not empty")
    return render(request,"Summary/index.html",{'history_qs':currUserHistory})

def getReport(request):
    allUserHistory=HistoryData.objects.all()

    user=User.objects.get(username=request.user)
    name=user.username
    print("Username is: ",name)
    currUserHistory=allUserHistory.filter(uname=name)
    print("User history is: ",currUserHistory)

    disease_name_filter=request.GET.get("disease_name_filter")
    date_filter=request.GET.get("date_filter")
    date_criteria=request.GET.get("date")
    medicine_name_filter=request.GET.get("medicine_name_filter")
    outcome_filter=request.GET.get("outcome")

    # Name filter
    if disease_name_filter!='' and disease_name_filter is not None:
        print("Disease Name Filter On")
        currUserHistory=currUserHistory.filter(infection__icontains=disease_name_filter)

    # Date filter
    if date_filter!='' and date_filter is not None:
        print("Date Filter On")
        if date_criteria=='before':
            currUserHistory=currUserHistory.filter(start_date__lt=date_filter)
        if date_criteria=='after':
            currUserHistory=currUserHistory.filter(start_date__gt=date_filter)
    
    # Medicine Name filter
    if medicine_name_filter!='' and medicine_name_filter is not None:
        print("Medicine Name Filter On")
        currUserHistory=currUserHistory.filter(medicine__icontains=medicine_name_filter)
    
    # Outcome filter
    if outcome_filter!='' and outcome_filter is not None:
        print("Outcome Filter On")
        currUserHistory=currUserHistory.filter(outcome=outcome_filter)

    
    buf=io.BytesIO()
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)

    lines=[]

    hist_data=HistoryData.objects.all()
    hist_data=hist_data.filter(uname=name)

    print(hist_data)

    for item in currUserHistory:
        lines.append(item.infection)
        lines.append(str(item.start_date))
        lines.append(str(item.end_date))
        lines.append(str(item.duration))
        lines.append(str(item.medicine))
        lines.append(str(item.outcome))
        lines.append("  ")


    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf,as_attachment=True,filename='healthreport.pdf')