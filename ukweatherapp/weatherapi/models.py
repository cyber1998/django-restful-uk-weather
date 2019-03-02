import datetime
from django.db import models

# Create your models here.


class Location(models.Model):

    objects = models.Manager()

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Metric(models.Model):

    objects = models.Manager()

    name = models.CharField(max_length=100)
    locations = models.ManyToManyField(Location, related_name='location')

    def __str__(self):
        return self.name


class Weather(models.Model):

    objects = models.Manager()

    # year = models.IntegerField(default=1901)
    # month = models.IntegerField(default=1)
    measured_at = models.DateField(default=datetime.date.today())
    value = models.FloatField()
    metric = models.ForeignKey(Metric, default=1, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, default=1, on_delete=models.CASCADE)
