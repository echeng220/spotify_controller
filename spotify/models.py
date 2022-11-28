from django.db import models
from api.models import Room


class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    refreshToken = models.CharField(max_length=150)
    accessToken = models.CharField(max_length=150)
    expiresIn = models.DateTimeField()
    tokenType = models.CharField(max_length=50)


class Vote(models.Model):
    user = models.CharField(max_length=50, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    songId = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
