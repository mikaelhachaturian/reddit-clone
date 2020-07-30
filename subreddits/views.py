from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Subreddit, Post, Comment, CommentVote, PostVote
from .forms import SubrForm, PostForm, CommentForm
from django.db import IntegrityError
from django.urls import reverse


def index(request):
    subs = Subreddit.objects.all()
    return render(request, 'subreddits/index.html', context={'subs': subs})


@login_required
def subr_creation_form(request):
    if request.method == 'POST':
        form = SubrForm(request.POST)
        if form.is_valid():
            subr = Subreddit(
                name=form.cleaned_data['name'], url_name=form.cleaned_data['name'].replace(" ", ""))
            subr.save()
            return redirect('subreddits:subr_view', subr_url_name=subr.url_name)
    else:
        form = SubrForm()

    return render(request, 'subr_creation_form/create_form.html', {'form': form})


@login_required
def post_creation_form(request):
    subs = Subreddit.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            subr = get_object_or_404(Subreddit, pk=form.cleaned_data["subs"])
            post = Post(
                name=form.cleaned_data['name'], created_by=request.user.username, text=form.cleaned_data['text'], subr=subr)
            post.save()
            return redirect('subreddits:post_view', post_id=post.pk)
    else:
        form = PostForm()

    return render(request, 'post_creation_form/create_post.html', {'form': form})


def subr_view(request, subr_url_name):
    subr = get_object_or_404(Subreddit, url_name=subr_url_name)
    posts = subr.post_set.order_by('-date_created')
    return render(request, 'subreddits/subr_view.html', context={'subr': subr, 'posts': posts})


def post_view(request, post_id, comment_id='', vote_type=''):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        post = Post.objects.get(id=post_id)
        if form.is_valid():
            comment = Comment(
                text=form.cleaned_data['text'], created_by=request.user.username, post=post)
            comment.save()
            return redirect('subreddits:post_view', post_id=post_id)
    else:
        if not request.user.is_authenticated:
            return redirect('login_view')
        elif comment_id:  # Comment Vote Section

            if vote_type == 'upvote':
                vote_int = 1
            elif vote_type == 'downvote':
                vote_int = -1

            try:
                vote = CommentVote(user=request.user,
                                   comment=Comment.objects.get(id=comment_id), vote_int=vote_int)
                vote.save()
            except IntegrityError as e:
                vote_update = CommentVote.objects.get(
                    comment=Comment.objects.get(id=comment_id), user=request.user)
                if (vote_type == 'upvote' and vote_update.vote_int == 1) or (vote_type == 'downvote' and vote_update.vote_int == -1):
                    vote_update.vote_int = 0
                else:
                    vote_update.vote_int = vote_int

                vote_update.save(update_fields=["vote_int"])
            return redirect(reverse('subreddits:post_view', kwargs={'post_id': post_id}) + '#comment-view-{}'.format(comment_id))
        elif vote_type:  # Post Comment Section
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
            return redirect('subreddits:post_view', post_id=post_id)
        else:
            post = get_object_or_404(Post, id=post_id)
            comments = post.comment_set.order_by('-date_created')
            form = CommentForm()
            return render(request, 'subreddits/post_view.html', context={'form': form, 'post': post, 'comments': comments})
