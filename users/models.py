from django.db import models
from artist.models import Artist
from artwork.models import Artwork
from PixivProxy.settings import COOKIES_DIRS
import re
from base64 import b64decode
from utils.pixivc import GetInfoByIdUnLogin
# Create your models here.


class User(models.Model):
    userName = models.CharField(max_length=40)
    userAccount = models.CharField(max_length=40)
    salt = models.CharField(max_length=40)
    token = models.CharField(max_length=40)
    userCookies = models.CharField(max_length=16)
    admission = models.BooleanField()
    pixivPassword = models.CharField(max_length=30)
    userId = models.DecimalField(max_digits=15, decimal_places=0)
    updateCollections = models.BooleanField()
    workMark = models.DecimalField(max_digits=6, decimal_places=0)

    def getCookies(self):
        fp = open(COOKIES_DIRS+'toyBox/'+self.userCookies, 'rb')
        cookies = b64decode(fp.read())
        fp.close()
        return cookies.decode()

    def setCookies(self, content):
        fp = open(COOKIES_DIRS+'toyBox/'+self.userCookies, 'wb')
        fp.write(content)
        fp.close()

    def setId(self, cookiesText):
        modeString = 'user_id=(.*?)='
        modeString = re.compile(modeString)
        self.userId = int(modeString.findall(cookiesText)[0])
        self.save()

    def ifmarked(self, picid):
        insId=GetInfoByIdUnLogin(picid,returnIns=True).id
        picList=self.bookmarkartwork_set.filter(target_id=insId)
        if not picList:
            return False
        return True

    def __str__(self):
        return self.userAccount


class bookMarkArtwork(models.Model):
    order = models.DecimalField(max_digits=6, decimal_places=0)
    marker = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Artwork, on_delete=models.CASCADE)


class bookMarkArtist(models.Model):
    marker = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Artist, on_delete=models.CASCADE)
