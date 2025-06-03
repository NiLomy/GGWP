from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from index import get_transformer, get_index, save_index


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    storyline = models.TextField(blank=True)
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


@receiver(post_save, sender=Game)
def game_post_save(sender, instance, **kwargs):
    summary = f"{instance.description} {instance.storyline}"
    embedding = get_transformer().encode(summary)

    index = get_index()
    index.add_item(embedding, id=instance.id)
    save_index(index)


@receiver(post_delete, sender=Game)
def game_post_delete(sender, instance, **kwargs):
    index = get_index()
    index.mark_deleted(id=instance.id)
    save_index(index)
