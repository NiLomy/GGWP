from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    image_url = models.CharField(max_length=512, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='games')

    def __str__(self):
        return self.name


class UserGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game')
