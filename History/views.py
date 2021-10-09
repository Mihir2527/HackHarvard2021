from django.shortcuts import render
from History.models import HistoryData
from django.contrib.auth.models import User

# Create your views here.

def getHistoryPage(request):
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
    outcome_filter=request.GET.get("outcome_filter")

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