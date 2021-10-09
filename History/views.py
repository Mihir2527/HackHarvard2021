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

    # if not allUserHistory:
    #     print("empty")
    #     return render(request,"History/index.html")
    # else:
    #     print("not empty")
    return render(request,"History/index.html",{'history_qs':currUserHistory})