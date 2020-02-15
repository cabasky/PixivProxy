from django.shortcuts import render
from django.http import HttpResponse
from artist.models import Artist
from artwork.models import Artwork
from ranklist.models import RankList,RankWork,Edge 
from utils.pixivc import bookMarkOnArtwork
from users.models import User 
# Create your views here.

def delall(request):
    Artwork.objects.all().delete()
    Artist.objects.all().delete()
    RankWork.objects.all().delete()
    RankList.objects.all().delete()
    Edge.objects.all().delete()
    return HttpResponse('del OK!')

def testtemp(request):
    return HttpResponse(bookMarkOnArtwork(User.objects.get(id=1),'79286371'),content_type='application/json')