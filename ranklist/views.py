from django.shortcuts import render
from utils.ranking import loadranklist, rankpiece
from ranklist.models import RankList, RankWork, Edge
from django.utils import timezone
import datetime
# Create your views here.
userimgheader = 'https://i.pximg.net/user-profile/img/'


def ranklist(request):
    if timezone.now().hour < 12:
        deltadays = 2
    else:
        deltadays = 1
    datedefault = (timezone.now()-datetime.timedelta(days=deltadays)
                   ).strftime("%Y%m%d")
    if(request.POST):
        mode = int(request.POST['type'])
        rankdate = request.POST['date']
        if (not len(rankdate) == 8) or rankdate > datedefault:
            rankdate = datedefault
    else:
        rankdate = datedefault
        mode = 0
    rklstobj = RankList.objects.filter(rankdate=rankdate, mode=mode)
    rkl = []
    if(not rklstobj):
        rkl = loadranklist(requestdate=rankdate, mode=mode)
        rklstobj = RankList(mode=mode, rankdate=rankdate)
        rklstobj.save()
        for r in rkl:
            w = RankWork.objects.filter(artworkid=r.id)
            if(not w):
                w = RankWork(artworkid=r.id, artist=r.artist,
                             name=r.name, artistid=r.artistid)
                w.save()
            else:
                w = w[0]
            edg = Edge(rankl=rklstobj, rankw=w, ranking=r.rnk)
            edg.save()
        if len(rkl) < 100:
            rklstobj.delete()
    else:
        rklstobj = rklstobj[0]
        rklraw = rklstobj.edge_set.all().order_by('ranking')
        for i in rklraw:
            rkl.append(rankpiece(id=i.rankw.artworkid, name=i.rankw.name, artist=i.rankw.artist, artistid=i.rankw.artistid))
    context = {'rankdate': rankdate,
               'mode': rklstobj.get_mode_display(), 'rkl': rkl}
    return render(request, template_name='ranklist/ranklist.html', context=context)
