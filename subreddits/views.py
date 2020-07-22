from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Subreddit, Post, Comment
from .forms import SubrForm, PostForm, CommentForm


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
def post_creation_form(request, subr_url_name):
    if request.method == 'POST':
        subr = Subreddit.objects.get(url_name=subr_url_name)
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(
                name=form.cleaned_data['name'], created_by=request.user.username, text=form.cleaned_data['text'], subr=subr)
            post.save()
            return redirect('subreddits:subr_view', subr_url_name=subr.url_name)
    else:
        form = PostForm()

    return render(request, 'post_creation_form/create_post.html', {'form': form, 'subr_url_name': subr_url_name})


def subr_view(request, subr_url_name):
    subr = get_object_or_404(Subreddit, url_name=subr_url_name)
    posts = subr.post_set.order_by('-date_created')
    return render(request, 'subreddits/subr_view.html', context={'subr': subr, 'posts': posts})


def post_view(request, post_id):
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
        else:
            post = get_object_or_404(Post, id=post_id)
            comments = post.comment_set.order_by('-date_created')
            form = CommentForm()
            return render(request, 'subreddits/post_view.html', context={'form': form, 'post': post, 'comments': comments})
