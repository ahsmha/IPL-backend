from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.CharField(max_length=100, unique=True)
    owner = models.CharField(max_length=200)
    coach = models.CharField(max_length=100)
    captain = models.CharField(max_length=100)
    winning_seasons = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = 'teams'
