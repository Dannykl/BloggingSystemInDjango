from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
from taggit.models import Tag
from django.db.models import Count

class PostListView(ListView):

    template = 'blog/list.html'
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = template

# tag_slug (tag) is optional parameter
def post_list(request, tag_slug=None):
    template = 'blog/list.html'
    list_of_objects = Post.published.all()
    tag = None
    # the bellow if statement is only executed if the optional parameter, tag_slug, is given
    if(tag_slug):
        tag = get_object_or_404(Tag,slug=tag_slug)
        # filter the posts that have the given tag
        list_of_objects = list_of_objects.filter(tags__in=[tag])
    #set 3 posts in the page
    paginator = Paginator(list_of_objects,4)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # deliver the first page if page is not an integer
        posts = paginator.page(1)
    except EmptyPage:
        # deliver the last page of the result if the page is out of range
        posts = paginator.page(paginator.num_pages)

    return render (request,template,{'page':page,'posts':posts,'tag':tag})


def post_detail(request, year,month,day,post):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # list of active comments for this post
    comments = post.comments.filter(active=True)

    if(request.method=='POST'):
        # comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object but do not save it in the database
            new_comment = comment_form.save(commit=False)

            #Assign the current post to the comment
            new_comment.post = post

            #save the comment in the database
            new_comment.save()

    else:
        comment_form = CommentForm()

    # list similar posts
    post_tag_ids = Post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags','-publish')[:5]
    return render(request,template,{'post':post,
                                    'comments':comments,
                                    'comment_form':comment_form,
                                    'similar_posts':similar_posts})

def post_share(request,post_id):

    template = 'blog/share.html'
    # retrieve post by id
    post = get_object_or_404(Post,id=post_id,status='published')
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




