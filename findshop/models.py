from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.name


