from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .utils import paginator
from .forms import PostForm
from .models import Post, Group, User


def index(request):
    # select_related получает связанные объекты в том же запросе к базе данных
    # Сверху была цитата с сайта, на который вы кинули ссылку.
    # В этой функции у меня нет никаких связанных данных
    # Мне нужны все посты, но никаких других данных доставать не нужно
    post_list = Post.objects.select_related(
        'group', 'author').all()
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related(
        'group', 'author').all()
    page_obj = paginator(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    postes = author.posts.select_related('group').all()
    count = postes.count()
    page_obj = paginator(request, postes)
    context = {
        'count': count,
        'author': author,
        'page_obj': page_obj,

    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)
