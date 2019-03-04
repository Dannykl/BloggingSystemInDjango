from django.shortcuts import render,get_object_or_404
from .models import Post


def post_list(request):
    template = 'blog/list.html'
    posts = Post.published.all()
    return render(request,template,{'posts':posts})


def post_detail(request, year,month,day,post):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,template,{'post':post})

