from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404
from .models import Post as p
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm

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

def post_share(request,post_id):

    template = 'blog/share.html'
    # retrieve post by id
    post = get_object_or_404(p,id=post_id,status='published')
    sent = False

    if request.method == "POST":
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields are passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])

            send_mail(subject, message, 'danielniguse88@gmail.com',[cd['to']])

            sent = True

    else:
        form = EmailPostForm()
    return render(request,template,{'post':post, 'form':form, 'sent':sent})




