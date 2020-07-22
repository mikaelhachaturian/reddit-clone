from django.db import models
from django.utils import timezone


class Subreddit(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url_name = models.CharField(max_length=30, default=None)
    date_created = models.DateTimeField(default=timezone.now)


class Post(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    subr = models.ForeignKey(Subreddit, on_delete=models.CASCADE)


class Comment(models.Model):
    text = text = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
