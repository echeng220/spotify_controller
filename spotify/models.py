from django.db import models


class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    refreshToken = models.CharField(max_length=150)
    accessToken = models.CharField(max_length=150)
    expiresIn = models.DateTimeField()
    tokenType = models.CharField(max_length=50)
