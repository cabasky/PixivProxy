#from pixivc import GetInfoByIdUnLogin,GetpicturebyUrl
import json
import requests
modestr = ['daily', 'weekly', 'monthly', 'rookie', 'male', 'female']


class rankpiece:
    def __init__(self, id, name, artist, artistid, rnk=0):
        self.id = id
        self.name = name
        self.artist = artist
        self.rnk = rnk
        self.artistid = artistid


def loadranklist(requestdate, mode):
    totalrank = 0
    page = 1
    ranklist = []
    while True:
        requrl = 'https://www.pixiv.net/ranking.php?mode=%s&date=%s&p=%d&format=json' % (
            modestr[mode], requestdate, page)
        page += 1
        jsonstr = requests.get(url=requrl).text
        rankpage = json.loads(jsonstr)['contents']
        for r in rankpage:
            ranklist.append(rankpiece(
                name=r['title'], artist=r['user_name'], id=int(r['illust_id']), rnk=totalrank, artistid=int(r['user_id'])))
            totalrank += 1
            if totalrank>99:
                break
        if totalrank>99:
            break
    return ranklist
