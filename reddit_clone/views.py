from django.shortcuts import render
from subreddits.models import Subreddit, Post


def home(request):
    posts = Post.objects.order_by('-date_created')
    return render(request, 'home.html', context={'posts': posts})
