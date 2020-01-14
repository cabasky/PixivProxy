from django.db import models

# Create your models here.


class RankList(models.Model):
    ranktype = (
        (0, 'daily'),
        (1, 'weekly'),
        (2, 'monthly'),
        (3, 'rookie'),
        (4, 'male'),
        (5, 'female'),
    )
    mode = models.IntegerField(choices=ranktype)
    rankdate = models.CharField(max_length=8)
    def __str__(self):
        return self.rankdate+self.get_mode_display()


class RankWork(models.Model):
    artworkid = models.DecimalField(max_digits=10, decimal_places=0)
    name = models.CharField(max_length=40)
    artist = models.CharField(max_length=40)
    artistid=models.DecimalField(max_digits=10, decimal_places=0)

class Edge(models.Model):
    rankl = models.ForeignKey(RankList, on_delete=models.CASCADE)
    rankw = models.ForeignKey(RankWork, on_delete=models.CASCADE)
    ranking = models.DecimalField(max_digits=2, decimal_places=0)
    def __str__(self):
        return str(self.ranking)+'#'+str(self.rankw.artworkid)
