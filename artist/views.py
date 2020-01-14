from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from utils.pixivc import *
from .models import Artist
import json
# Create your views here.


def artistimg(request, artistid, mode):
    url = Getartistimg(artistid=artistid, mode=mode)
    img, allowtype = GetpicturebyUrl(url)
    return HttpResponse(img, content_type=allowtype)


def artistinfo(request, artistid):
    idList = Artist.objects.filter(artistid=artistid)
    if(not idList):
        name = Getartistinfo(artistid)
        NewArtist = Artist(artistid=int(artistid), name=name)
        NewArtist.save()
    else:
        NewArtist = idList[0]
        name = NewArtist.name
    ret = {
        "artistid": artistid,
        "name": name
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')
