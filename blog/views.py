from django.shortcuts import render,get_object_or_404
from .models import Post as p
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView


class PostListView(ListView):

    template = 'blog/list.html'
    queryset = p.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = template

# def post_list(request):
#     template = 'blog/list.html'
#     list_of_objects = p.published.all()
#     #set 3 posts in the page
#     paginator = Paginator(list_of_objects,4)
#     page = request.GET.get('page')
#
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # deliver the first page if page is not an integer
#         posts = paginator.page(1)
#     except EmptyPage:
#         # deliver the last page of the result if the page is out of range
#         posts = paginator.page(paginator.num_pages)
#
#     return render (request,template,{'page':page,'posts':posts})


def post_detail(request, year,month,day,post):
    template = 'blog/detail.html'
    post = get_object_or_404(p, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,template,{'post':post})

