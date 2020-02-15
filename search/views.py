from django.shortcuts import render
from django.http import HttpResponseRedirect
from utils.pixivc import *
from users.models import User
# Create your views here.


def searchpage(request):
    print(request.session.get('logged', False))
    if not request.session.get('logged', False):
        print(1)
        logged = False
        userName = ''
    else:
        print(2)
        logged = True
        userName = User.objects.get(id=request.session['userId']).userName
    print(logged)
    ctx={
        'logged': logged,
        'userName': userName,
    }
    return render(
        request,
        context=ctx,
        template_name='search/IdSearch.html'
    )

def searchWork(request):
    if not request.session.get('logged', False):
        logged = False
        userName = ''
    else:
        logged = True
        userName = User.objects.get(id=request.session['userId']).userName
    if 'id' in request.POST:
        return HttpResponseRedirect('?keywords='+request.POST['id'])
    keyWords=request.GET['keywords']
    if 'p' in request.GET :
        p=int(request.GET['p'])
    else:
        p=0
    workList,totalSum=GetSearchList(keyWords,p)
    pages=pagelist(totalSum//15,p+1)
    ctx={
        'workList':workList,
        'Keywords':keyWords,
        'num':totalSum,
        'pages':pages,
        'logged': logged,
        'userName': userName,
    }
    return render(
        request,
        context=ctx,
        template_name='search/searchWork.html'
    )