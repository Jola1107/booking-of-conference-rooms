from django.db import models
from datetime import datetime, date


class Rooms(models.Model):
    name = models.CharField(max_length=255, unique=True)
    seats = models.IntegerField()
    projector = models.BooleanField(default=False)


class Reserve(models.Model):
    date = models.DateField()
    id_reserve = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    comment = models.TextField(null=True)

class Meta:
    unique_both = ('date', 'id_reserve')


