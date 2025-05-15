from django.db import models
from django.contrib.auth.models import AbstractUser

class Record_Calendar(models.Model):
    year = models.IntegerField()
    updated_at = models.DateField(blank=True, null=True)

class Games_Genres(models.Model):
    name = models.CharField(max_length=255)

class Games_Platforms(models.Model):
    name = models.CharField(max_length=50)

class Games_Data(models.Model):
    name = models.CharField(max_length=100)
    genres = models.ManyToManyField(Games_Genres, related_name="games_genres")
    release_date = models.DateField()
    platform = models.ManyToManyField(Games_Platforms, related_name="games_platforms")
    storyline = models.TextField()
    summary = models.TextField()
    cover_id = models.CharField(max_length=255)
    updated_at = models.ForeignKey(Record_Calendar, null=True, blank=True, on_delete=models.CASCADE, related_name="games_updated")
    record_year = models.ForeignKey(Record_Calendar, on_delete=models.CASCADE, related_name="games_record_year")

class User(AbstractUser):
    followed_games = models.ManyToManyField(Games_Data, related_name="followers")