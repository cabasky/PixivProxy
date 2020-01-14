from django.db import models
from artist.models import Artist
# Create your models here.


class Artwork(models.Model):
    formatchoice=(
        (0,'jpg'),
        (1,'png'),
    )
    picid = models.DecimalField(max_digits=10, decimal_places=0)
    picartist=models.ForeignKey(Artist,on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    url = models.CharField(max_length=25)
    pageCount=models.DecimalField(max_digits=2,decimal_places=0)
    imgformat = models.IntegerField(choices=formatchoice)
    def __str__(self):
        return self.name
