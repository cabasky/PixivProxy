import requests
# import json
import re
from artwork.models import Artwork
from artist.models import Artist
from users.models import bookMarkArtwork, User
import json
# from artwork.models import Artwork

imgheaders = 'accept: image/webp,image/apng,image/*,*/*;q=0.8|accept-encoding: gzip, deflate, br|accept-language: zh-CN,zh;q=0.9|referer: https://www.pixiv.net/|sec-fetch-mode: no-cors|sec-fetch-site: cross-site'

rc = 'p_ab_id=9; first_visit_datetime_pc=2019-07-29+00%3A32%3A46; p_ab_id_2=2; p_ab_d_id=1223278060; yuid_b=GTVIBIA; _ga=GA1.2.1792811796.1564327977; privacy_policy_agreement=1; c_type=29; a_type=0; b_type=1; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=22318221=1^9=p_ab_id=9=1^10=p_ab_id_2=2=1^11=lang=zh=1; ki_r=; __utmz=235335808.1564411602.3.2.utmcsr=cnblogs.com|utmccn=(referral)|utmcmd=referral|utmcct=/; device_token=f8b5a341a095a8df6bb61ec6ad7d4ae8; ki_s=201971%3A0.0.0.0.0; PHPSESSID=22318221_xgCtskekly10CXlvP0m3EzwXPyEf8z9J; ki_t=1564328343482%3B1575808164994%3B1575810786617%3B4%3B17; is_sensei_service_user=1; __utma=235335808.1792811796.1564327977.1575807302.1575958241.12; __utmc=235335808; __utmt=1; OX_plg=pm; tag_view_ranking=iFcW6hPGPU~EGefOqA6KB~VCG9z5cBNK~FaNMkYX7dX~D0nMcn6oGk~iajmMoolkv~wyZOlBKxtg~WlKkwEuUi0~QviSTvyfUE; __utmb=235335808.2.10.1575958241; tags_sended=1; categorized_tags=CADCYLsad0~EGefOqA6KB~iFcW6hPGPU'

urlset = [
    ('https://i.pximg.net/c/48x48/img-master/img/', '_square1200.jpg'),
    ('https://i.pximg.net/c/128x128/img-master/img/', '_square1200.jps'),
    ('https://i.pximg.net/c/250x250_80_a2/img-master/img/', '_square1200.jpg'),
    ('https://i.pximg.net/c/540x540_70/img-master/img/', '_master1200.jpg'),
    ('https://i.pximg.net/img-master/img/', '_master1200.jpg'),
    ('https://i.pximg.net/img-original/img/', '.'),
]


artistimgset = [
    'image',
    'imageBig',
]


class Cookies:
    rawcookies = ''
    cookiesdict = {}

    def init(self, cstr):
        rawcookies = cstr.replace(' ', '')
        for i in rawcookies.split(';'):
            a, b = i.split('=', 1)
            self.cookiesdict[a] = b

    def __init__(self, cstr=None):
        if cstr == None:
            return
        else:
            rawcookies = cstr.replace(' ', '')
            for i in rawcookies.split(';'):
                a, b = i.split('=', 1)
                self.cookiesdict[a] = b


class Headers:
    rawheaders = ''
    headersdict = {}

    def __init__(self, hstr):
        rawheaders = hstr.replace(' ', '')
        for i in rawheaders.split('|'):
            a, b = i.split(':', 1)
            self.headersdict[a] = b


class PixivClient:
    UserCookieDict = Cookies()
    Live = requests.Session()
    MainPage = None
    ImgHeaders = Headers(imgheaders)

    def login(self, cstr):
        self.UserCookieDict.init(cstr)
        self.MainPage = self.Live.get(
            url='https://www.pixiv.net', cookies=self.UserCookieDict.cookiesdict)

    def GetPictureById(self, id, mode, filedict):
        MainUrl = 'https://www.pixiv.net/artworks/'+id
        ArtworkPage = self.Live.get(
            url=MainUrl, cookies=self.UserCookieDict.cookiesdict)
        PicQuality = PictureMode[mode]
        ModePattern = PicQuality+'.*?:.*?(https.*?jpg)'
        Modere = re.compile(ModePattern)
        PictUrl = Modere.findall(ArtworkPage.text)[0]
        op = open(filedict, "wb")
        img = self.Live.get(url=PictUrl, headers=self.ImgHeaders.headersdict)
        op.write(img.content)
        op.close()

    def __del__(self):
        self.close()


def GetInfoByIdUnLogin(id, InsArtist=None, returnIns=False):
    idList = Artwork.objects.filter(picid=int(id))
    if(not idList):
        mainjson = requests.get('https://www.pixiv.net/ajax/illust/'+id).text
        mainjson = json.loads(mainjson)['body']
        if InsArtist == None:
            InsArtistId = int(mainjson['userId'])
            InsArtist = Artist.objects.filter(artistid=InsArtistId)
            if not InsArtist:
                InsArtist = Artist(
                    name=mainjson['userName'], artistid=InsArtistId)
                InsArtist.save()
            else:
                InsArtist = InsArtist[0]
        InsName = mainjson['illustTitle']
        InsPageCount = int(mainjson['pageCount'])
        InsUrl = mainjson['urls']['original']
        if 'jpg' in InsUrl:
            Insformat = 0
        elif 'png' in InsUrl:
            Insformat = 1
        modestr = re.compile('img/(.*?/)'+id)
        InsUrl = modestr.findall(InsUrl)[0]
        NewArtwork = Artwork(picid=int(id), picartist=InsArtist, name=InsName,
                             url=InsUrl, pageCount=InsPageCount, imgformat=Insformat)
        NewArtwork.save()
    else:
        NewArtwork = idList[0]
        InsArtist = NewArtwork.picartist
        InsName = NewArtwork.name
        InsUrl = NewArtwork.url
        InsPageCount = NewArtwork.pageCount
        Insformat = NewArtwork.imgformat
    if(returnIns):
        return NewArtwork
    return (str(InsArtist.artistid), InsArtist.name, InsName, InsUrl, InsPageCount, Insformat)


def Getpicurl(rawurl, id, mode, page, imgformat):
    if mode == 5:
        ret = urlset[mode][0]+rawurl+id+'_p' + \
            str(page)+urlset[mode][1]+imgformat
    else:
        ret = urlset[mode][0]+rawurl+id+'_p'+str(page)+urlset[mode][1]
    return ret


def GetpicturebyUrl(url):
    if 'png' in url:
        allowtype = 'image/png'
    elif 'gif' in url:
        allowtype = 'image/gif'
    elif 'jpg' in url:
        allowtype = 'image/jpg'
    img = requests.get(url=url, headers=Headers(imgheaders).headersdict)
    return img, allowtype


def Getartistinfo(artistid, update=0, pg=0):
    idList = Artist.objects.filter(artistid=artistid)
    if(not idList):
        mainjson = requests.get(
            'https://www.pixiv.net/ajax/user/'+artistid, cookies=Cookies(rc).cookiesdict).text
        mainjson = json.loads(mainjson)['body']
        name = mainjson['name']
        NewArtist = Artist(artistid=int(artistid), name=name)
        NewArtist.save()
    else:
        NewArtist = idList[0]
        name = NewArtist.name
    if not update:
        return name
    else:
        mainjson = json.loads(requests.get(
            'https://www.pixiv.net/ajax/user/'+artistid, cookies=Cookies(rc).cookiesdict).text)['body']
        if mainjson['background'] == None:
            isbkg = 0
        else:
            isbkg = 1
        if mainjson['premium'] == True:
            isprem = 1
        else:
            isprem = 0
        mainurl = 'https://www.pixiv.net/ajax/user/'+artistid+'/profile/all'
        mainjson = list(json.loads(requests.get(
            mainurl).content)['body']['illusts'])
        step = 15
        s = pg*step
        l = len(mainjson)
        namelist = []
        for i in range(step):
            if i+s >= l:
                break
            namelist.append((mainjson[i+s], GetInfoByIdUnLogin(
                mainjson[i+s], InsArtist=NewArtist)[2]))
        if s+step >= l:
            t = l
        else:
            t = s+step
        return name, namelist, l, isbkg, isprem


def Getartistimg(artistid, mode):
    mainjson = requests.get(
        'https://www.pixiv.net/ajax/user/'+artistid, cookies=Cookies(rc).cookiesdict).text
    return json.loads(mainjson)['body'][artistimgset[mode]]


def Getbackground(artistid):
    mainjson = requests.get(
        'https://www.pixiv.net/ajax/user/'+artistid, cookies=Cookies(rc).cookiesdict).text
    return json.loads(mainjson)['body']['background']


def pagelist(tot, active):
    l = [active]
    lflag = 0
    rflag = 0
    if active > 1:
        l = [active-1]+l
        lflag = 1
    if active < tot:
        l += [active+1]
        rflag = 1
    if active > 2 and active < 4:
        l = [active-2]+l
    if active < tot-1:
        l += [active+2]

    if active > 3 and active < 4:
        l = [active-2]+l
    if active < tot-2:
        l += [active+3]
    return (active, lflag, rflag, l)


def GetSearchList(keywords, page):
    webPage = (page//4)+1
    mainUrl = 'https://www.pixiv.net/ajax/search/artworks/%s?word=%s&order=date_d&mode=all&p=%d&s_mode=s_tag&type=all' % (
        keywords, keywords, webPage)
    mainJson = json.loads(requests.get(mainUrl).content)['body']['illustManga']
    startTag = (page % 4)*15
    totalNum = mainJson['total']
    mainJson = list(mainJson['data'])
    l = len(mainJson)
    workList = []
    for i in range(15):
        if i + startTag >= l:
            break
        if mainJson[i+startTag]['isAdContainer']:
            continue
        workList.append((mainJson[i+startTag]['id'],
                         mainJson[i+startTag]['title']))
    return workList, totalNum


def getUserDiscovery(userClass):
    mainUrl = 'https://www.pixiv.net/rpc/recommender.php?type=illust&sample_illusts=auto&num_recommendations=15&page=discovery&mode=all'
    cookies = Cookies(userClass.getCookies()).cookiesdict
    headers = Headers('accept: */*|accept-encoding: gzip, deflate, br|accept-language: zh-CN,zh;q=0.9|referer: https://www.pixiv.net/discovery|sec-fetch-dest: empty|sec-fetch-mode: cors|sec-fetch-site: same-origin|user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36|x-user-id: '+str(userClass.userId)).headersdict
    mainJson = json.loads(requests.get(
        url=mainUrl, cookies=cookies, headers=headers).text)
    return mainJson['recommendations']


def getUserCollections(userClass, offset):
    totalNum = userClass.workMark
    st = totalNum-offset
    workList = []
    for i in range(15):

        if st == 0:
            break
        workList.append(str(userClass.bookmarkartwork_set.all().get(
            order=st).target.picid))
        st -= 1
    return workList, totalNum


def updateUserCollections(userClass):
    cookies = Cookies(userClass.getCookies()).cookiesdict
    headers = Headers('accept: application/json|accept-encoding: gzip, deflate, br|accept-language: zh-CN,zh;q=0.9|referer: https://www.pixiv.net/users/%d/bookmarks/artworks|sec-fetch-dest: empty|sec-fetch-mode: cors|sec-fetch-site: same-origin|user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36|x-user-id: %d' % (userClass.userId, userClass.userId)).headersdict
    offset = 0
    num = 0
    workList = []
    userClass.bookmarkartwork_set.all().delete()
    while True:
        mainUrl = 'https://www.pixiv.net/ajax/user/%d/illusts/bookmarks?tag=&offset=%d&limit=100&rest=show' % (
            userClass.userId, offset)
        mainJson = json.loads(requests.get(
            url=mainUrl, cookies=cookies, headers=headers).text)['body']['works']
        if not mainJson:
            break
        for i in mainJson:
            workList.insert(0, i['illustId'])
            num += 1
        offset += 100
    userClass.workMark = num
    userClass.save()
    num = 0
    for i in workList:
        work = GetInfoByIdUnLogin(i, returnIns=True)
        num += 1
        link = bookMarkArtwork(marker=userClass, target=work, order=num)
        link.save()


def getCsrfToken(userClass, picid):
    mainUrl = 'https://www.pixiv.net/artworks/'+picid
    cookies = Cookies(userClass.getCookies()).cookiesdict
    headers = Headers('accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9|accept-encoding: gzip, deflate, br|accept-language: zh-CN,zh;q=0.9|cache-control: max-age=0|referer: https://www.pixiv.net/|sec-fetch-dest: document|sec-fetch-mode: navigate|sec-fetch-site: same-origin|sec-fetch-user: ?1|upgrade-insecure-requests: 1|user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36').headersdict
    mode = 'content=\'\{\"token\":\"(.*?)\"'
    text = requests.get(url=mainUrl, cookies=cookies, headers=headers).text
    mode = re.compile(mode)
    return mode.findall(text)[0]


def bookMarkArtworkInDB(userClass, picid):
    work = Artwork.objects.get(picid=picid)
    totalNum = userClass.workMark
    totalNum += 1
    link = bookMarkArtwork(marker=userClass, target=work, order=totalNum)
    link.save()
    userClass.workMark = totalNum
    userClass.save()


def bookMarkOnArtwork(userClass, picid):
    csrfToken = getCsrfToken(userClass, picid)
    mainUrl = 'https://www.pixiv.net/ajax/illusts/bookmarks/add'
    cookies = Cookies(userClass.getCookies()).cookiesdict
    headers = Headers('accept: application/json|accept-encoding: gzip, deflate, br|accept-language: zh-CN,zh;q=0.9|content-length: 60|content-type: application/json; charset=utf-8|origin: https://www.pixiv.net|referer: https://www.pixiv.net/artworks/%s|sec-fetch-dest: empty|sec-fetch-mode: cors|sec-fetch-site: same-origin|user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36|x-csrf-token: %s' % (picid, csrfToken)).headersdict
    payload = json.dumps(
        {'illust_id': picid, 'restrict': 0, 'comment': "", 'tags': []})
    mainJson = json.loads(requests.post(
        mainUrl, payload, cookies=cookies, headers=headers).content)
    if mainJson['body']['last_bookmark_id']:
        bookMarkArtworkInDB(userClass, picid)
        return True
    return False
