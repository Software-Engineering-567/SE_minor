from django.db import models

from django.db import models


class Bar(models.Model):
    bar_name = models.CharField(max_length=200)
    bar_rating = models.FloatField(default=0.0)
    bar_occupancy = models.IntegerField(default=0)
    bar_capacity = models.IntegerField(default=0)

