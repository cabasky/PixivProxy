from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
import hashlib
from utils.basictools import randstr
from PixivProxy.settings import COOKIES_DIRS
from utils.pixivc import Headers, Cookies, getUserDiscovery, getUserCollections, bookMarkOnArtwork
import json


def register(request):
    if request.session.get('logged', False):
        return HttpResponseRedirect('/user')

    if 'usr' in request.POST:
        usr = request.POST['usr']
        pwd = request.POST['pwd']
        cpwd = request.POST['cpwd']
        if not pwd == cpwd:
            return HttpResponse('Please confirm your password!')
        else:
            userList = User.objects.filter(userAccount=usr)
            if not userList:
                salt = randstr(32)
                pwd = salt+pwd
                token = hashlib.md5(pwd.encode()).hexdigest()
                userList = User(userName='', userAccount=usr, salt=salt,
                                token=token, userCookies=randstr(16), admission=False, userId=0, workMark=0, updateCollections=False, pixivPassword='')
                userList.save()
                return HttpResponse('Succeed!')
            else:
                return HttpResponse('The email had been used!')
    else:
        ctx = {
            'logged': False,
            'userName': '',
        }
        return render(request, template_name='user/register.html', context=ctx)


def login(request):
    if request.session.get('logged', False):
        return HttpResponseRedirect('/user')
    if 'usr' in request.POST:
        usr = request.POST['usr']
        pwd = request.POST['pwd']
        userList = User.objects.filter(userAccount=usr)
        if not userList:
            return HttpResponse('Account doesn\'t exist!')
        pwd = userList[0].salt+pwd
        tempToken = hashlib.md5(pwd.encode()).hexdigest()
        if not tempToken == userList[0].token:
            return HttpResponse('Wrong password!')
        request.session['logged'] = True
        request.session['userId'] = userList[0].id
        return HttpResponse('Successfully logged in!')
    return render(request, template_name='user/login.html')


def logout(request):
    request.session.flush()
    return HttpResponse('You\'ve logged out.')


def userMainPage(request):
    if not request.session.get('logged', False):
        return HttpResponseRedirect('login')
    userId = request.session['userId']  # system model ID
    mainUser = User.objects.get(id=userId)
    if 'pwd' in request.POST:
        pwd = request.POST['pwd']
        mainUser.pixivPassword = pwd
        mainUser.userName = request.POST['nic']
        mainUser.save()
        return HttpResponse('Please wait administrator.')
    if not mainUser.admission:
        return render(request, template_name='user/unadmitted.html')
    workList = getUserDiscovery(mainUser)
    ctx = {
        'logged': True,
        'userName': mainUser.userName,
        'userId': mainUser.userId,
        'workList': workList,
    }
    return render(request, template_name='user/userMainPage.html', context=ctx)


def discoveryRefresh(request):
    userId = request.session['userId']
    mainUser = User.objects.get(id=userId)
    workList = getUserDiscovery(mainUser)
    mainJson = json.dumps({'workList': workList})
    return HttpResponse(mainJson, content_type='application/json')


def collectionAppend(request):
    userId = request.session['userId']
    mainUser = User.objects.get(id=userId)
    offset = int(request.GET['offset'])
    workList = getUserCollections(mainUser, offset)[0]
    mainJson = json.dumps({'workList': workList})
    return HttpResponse(mainJson, content_type='application/json')


def userCollection(request):
    if not request.session.get('logged', False):
        return HttpResponseRedirect('/user/login')
    userId = request.session['userId']
    mainUser = User.objects.get(id=userId)
    workList, totalNum = getUserCollections(mainUser, 0)
    ctx = {
        'userName': mainUser.userName,
        'userId': mainUser.userId,
        'workList': workList,
        'num': totalNum,
        'logged': True,
    }
    return render(request, template_name='user/collections.html', context=ctx)


def addBookMarkWork(request):
    if not request.session.get('logged', False):
        return HttpResponse('Please login first!')
    userId = request.session['userId']  # system model ID
    mainUser = User.objects.get(id=userId)
    picid = request.POST['picid']
    if bookMarkOnArtwork(mainUser, picid):
        return HttpResponse('Success!')
    return HttpResponse('Unknown error!')
