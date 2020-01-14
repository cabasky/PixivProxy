from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from utils.pixivc import *
from .models import Artwork
import json
# Create your views here.
formatset = ['jpg','png']


def postid(request):
    return HttpResponseRedirect(request.POST['id'])


def ArtworkId(request, workid):
    ArtistId, Artist, Name, Url, PageCount, ImgFormat = GetInfoByIdUnLogin(str(workid))
    context = {'artworkid': workid, 'artist': Artist,
               'artistid': ArtistId, 'name': Name}
    return render(
        request,
        template_name='artwork/artworkpage.html',
        context=context
    )


def Artworkinfo(request, workid):
    idList = Artwork.objects.filter(picid=int(workid))
    if(not idList):
        ArtistId, Artist, Name, Url, PageCount, ImgFormat = GetInfoByIdUnLogin(
            id=workid)
        '''NewArtwork = Artwork(picid=int(workid), artist=Artist, artistId=int(
            ArtistId), url=Url, name=Name, pageCount=PageCount, imgformat=ImgFormat)
        NewArtwork.save()'''
    else:
        NewArtwork = idList[0]
        ArtistId = str(NewArtwork.picartist.artist)
        Artist = NewArtwork.picartist.name
        Name = NewArtwork.name
        Url = NewArtwork.url
        PageCount = str(NewArtwork.pageCount)
        ImgFormat = str(NewArtwork.imgformat)

    PicInfo = {
        'Artist': Artist,
        'Artistid': ArtistId,
        'Name': Name,
        'Url': Url,
        'PageCount': PageCount,
        'imgformat': ImgFormat,
    }
    return HttpResponse(json.dumps(PicInfo), content_type='application/json')


def img(request, workid, mode):
    idList = Artwork.objects.filter(picid=int(workid))
    if(not idList):
        raw = GetInfoByIdUnLogin(workid)
        url = Getpicurl(raw[3], workid, mode, 0, formatset[raw[5]])
    else:
        url = Getpicurl(idList[0].url, workid, mode, 0,
                        formatset[idList[0].imgformat])
    img, allowtype = GetpicturebyUrl(url)
    return HttpResponse(img, content_type='image/jpg;image/png')
