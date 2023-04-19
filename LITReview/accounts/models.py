from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class Ticket(models.Model):
    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    time_created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='following_by')
    unique_together = ['user', 'followed_user']
    objects = models.Manager()


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    # validates that rating must be between 0 and 5
    rating = models.PositiveSmallIntegerField(max_length=1024,
                                              validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.fields.CharField(max_length=128)
    body = models.fields.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
