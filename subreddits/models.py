from django.db import models
from django.utils import timezone
from django.conf import settings


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

    def votes_sum(self):
        votes = self.votes.all()
        sum = 0
        for vote in votes:

            sum += vote.post_int
        return sum


class PostVote(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'], name='unique_post_vote')
        ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name="votes", on_delete=models.CASCADE)

    post_int = models.IntegerField(default=0)


class Comment(models.Model):
    text = text = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def votes_sum(self):
        votes = self.votes.all()
        sum = 0
        for vote in votes:

            sum += vote.vote_int
        return sum


class CommentVote(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'comment'], name='unique_comment_vote')
        ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, related_name="votes", on_delete=models.CASCADE)

    vote_int = models.IntegerField(default=0)
