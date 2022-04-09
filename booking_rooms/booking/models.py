from django.db import models


class Rooms(models.Model):
    name = models.CharField(max_length=255, unique=True)
    seats = models.IntegerField()
    projector = models.BooleanField(default=False)


