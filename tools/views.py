from django.shortcuts import render
from django.http import HttpResponse
from artist.models import Artist
from artwork.models import Artwork
from ranklist.models import RankList,RankWork,Edge 
# Create your views here.

def delall(request):
    Artwork.objects.all().delete()
    Artist.objects.all().delete()
    RankWork.objects.all().delete()
    RankList.objects.all().delete()
    Edge.objects.all().delete()
    return HttpResponse('del OK!')

def testtemp(request):
    ctx={
        'pages':(1,0,1,[1,2])
    }
    return render(
        request,
        template_name='tpage.html',
        context=ctx,
    )