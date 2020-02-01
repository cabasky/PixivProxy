from django.shortcuts import render
from django.http import HttpResponseRedirect
from utils.pixivc import *
# Create your views here.


def searchpage(request):
    return render(
        request,
        template_name='search/IdSearch.html'
    )

def searchWork(request):
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
    }
    return render(
        request,
        context=ctx,
        template_name='search/searchWork.html'
    )