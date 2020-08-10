from django.shortcuts import render, redirect
from django.urls import reverse
from subreddits.models import Post, PostVote
from django.db import IntegrityError


def home(request, post_id='', vote_type=''):
    if vote_type:
        if vote_type == 'upvote':
            vote_int = 1
        elif vote_type == 'downvote':
            vote_int = -1

        try:
            vote = PostVote(user=request.user,
                            post=Post.objects.get(id=post_id), post_int=vote_int)
            vote.save()
        except IntegrityError as e:
            vote_update = PostVote.objects.get(
                post=Post.objects.get(id=post_id), user=request.user)
            if (vote_type == 'upvote' and vote_update.post_int == 1) or (vote_type == 'downvote' and vote_update.post_int == -1):
                vote_update.post_int = 0
            else:
                vote_update.post_int = vote_int

            vote_update.save(update_fields=["post_int"])
        return redirect(reverse('homepage') + '#post-view-{}'.format(post_id))
    else:
        posts = Post.objects.order_by('-date_created')
        return render(request, 'home.html', context={'posts': posts})
