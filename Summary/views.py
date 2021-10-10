from django.shortcuts import redirect, render
from History.models import HistoryData
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from django.http.response import HttpResponse

from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.utils import ImageReader
from reportlab.platypus.tables import Table
cm = 2.54

# Create your views here.
def getHomePage(request):
    allUserHistory=HistoryData.objects.all()

    user=User.objects.get(username=request.user)
    name=user.username
    print("Username is: ",name)
    currUserHistory=allUserHistory.filter(uname=name)
    print("User history is: ",currUserHistory)
    currUserHistory2=currUserHistory

    
    if 'gentable' in request.GET:
        inpyear=request.GET.get('year')
        currUserHistory2=currUserHistory.filter(start_date__contains=inpyear)


    # if not allUserHistory:
    #     print("empty")
    #     return render(request,"History/index.html")
    # else:
    #     print("not empty")

    month_dict={
        '01':'January',
        '02':'February',
        '03':'March',
        '04':'April',
        '05':'May',
        '06':'June',
        '07':'July',
        '08':'August',
        '09':'September',
        '10':'October',
        '11':'November',
        '12':'December',
    }

    summaryDict={
        'January':"",
        'February':"",
        'March':"",
        'April':"",
        'May':"",
        'June':"",
        'July':"",
        'August':"",
        'September':"",
        'October':"",
        'November':"",
        'December':"",
    }


    for item in currUserHistory2:
        temp=str(item.start_date)
        temp1=temp.split("-")[1] # month number
        print(temp1)
        print("All months and infections")
        month_str=month_dict[temp1]
        summaryDict[month_str]+=(item.infection)+",   "

    print(summaryDict)
    print(currUserHistory)

    context={
        'history_qs':currUserHistory,
        'summaryDict':summaryDict,
    } # has to be a dictionary

    # return render(request,"Summary/index.html",{'history_qs':currUserHistory,'summaryDict':summaryDict})
    return render(request,"Summary/index.html",context)

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

    currUserHistory=currUserHistory.order_by("-start_date")
    
    buf=io.BytesIO()
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)

    lines=""


    info1="Name of person: "+user.first_name+" "+user.last_name
    info2="Email: "+user.email
    
    lines.append(info1)
    lines.append(info2)
    lines.append("  ")
    lines.append("  ")
    lines.append("Report Summary")
    lines.append("  ")
    

    for item in currUserHistory:
        temp=item.infection+" -- "+str(item.start_date)+" -- "+item.duration+" -- "+"Medicine: "+item.medicine+" -- "+"Outcome: "+item.outcome
        # lines.append(item.infection)
        # lines.append(str(item.start_date))
        # lines.append(str(item.end_date))
        # lines.append(item.duration)
        # lines.append(item.medicine)
        # lines.append(item.outcome)
        lines.append(temp)
        lines.append("  ")

    textob.setTextOrigin(3,40)

    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf,as_attachment=True,filename='healthreport.pdf')

