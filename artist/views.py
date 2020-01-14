from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from utils.pixivc import *
from .models import Artist
import requests
import json
# Create your views here.


def postid(request):
    return HttpResponseRedirect(request.POST['id'])

def artistimg(request, artistid, mode):
    url = Getartistimg(artistid=artistid, mode=mode)
    img, allowtype = GetpicturebyUrl(url)
    return HttpResponse(img, content_type=allowtype)


def background(request, artistid):
    url = Getbackground(artistid)
    if url == None:
        return HttpResponse('None')
    url = url['url']
    img, allowtype = GetpicturebyUrl(url)
    if img == None:
        return HttpResponse('None')
    else:
        return HttpResponse(img, content_type=allowtype)


def artistinfo(request, artistid):
    name = Getartistinfo(artistid)
    ret = {
        "artistid": artistid,
        "name": name,
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')


def artistpage(request, artistid):
    if 'p' in request.GET:
        pg = int(request.GET['p'])
    else:
        pg = 0
    name, wlist, num, isbkg, isprem = Getartistinfo(artistid, update=1, pg=pg)
    pages=pagelist((num+14)//15,pg+1)
    ctx = {
        'artistid': artistid,
        'artistname': name,
        'wlist': wlist,
        'num': num,
        'page': pg,
        'isbkg': isbkg,
        'isprem': isprem,
        'pages': pages,
    }
    return render(
        request,
        template_name='artist/artist.html',
        context=ctx
    )
