from django.db import models

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=40)
    artistid = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.name + ' #'+str(self.artistid)
