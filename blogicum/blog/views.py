from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Category, Post

from datetime import datetime


def index(request):
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        Q(pub_date__lte=datetime.now())
        & Q(is_published=True)
        & Q(category__is_published=True)
    ).order_by('-pub_date')[:5]

    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(
        Post,
        Q(pub_date__lte=datetime.now())
        & Q(is_published=True)
        & Q(category__is_published=True),
        pk=id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, is_published=True, slug=category_slug
    )
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        category=category.id,
        is_published=True,
        pub_date__lte=datetime.now()
    )
    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)
