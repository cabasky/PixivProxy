from ranklist.models import*
RankList.objects.all().delete()
RankWork.objects.all().delete()

Edge.objects.all().delete()
exit()

from artwork.models import *
Artwork.objects.filter(picid=78491896).delete()
exit()