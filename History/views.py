from django.shortcuts import redirect, render
from History.models import HistoryData
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def getHistoryPage(request):

    if request.method=="POST":
        user=User.objects.get(username=request.user)
        name=user.username
        
        infection=request.POST.get('infection')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        medicine=request.POST.get('medicine')
        outcome=request.POST.get('outcome')

        newRecord=HistoryData(uname=name,infection=infection,start_date=start_date,end_date=end_date,medicine=medicine,outcome=outcome)
        newRecord.save()
        messages.success(request,"Record added!!")
        return redirect("/history")

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

    # if not allUserHistory:
    #     print("empty")
    #     return render(request,"History/index.html")
    # else:
    #     print("not empty")
    return render(request,"History/index.html",{'history_qs':currUserHistory})

def newRecordPage(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    return render(request,"History/newrecord.html")