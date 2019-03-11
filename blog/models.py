from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
        def get_queryset(self):
            return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=250)
    # Slug is a short label containing only letters,nums,underscore or hyphes.
    # slug is used to create user friendly URL,
    # takes unique_for_date, is used to create url using date
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    # author = models.ForeignKey(User, related_name='blog_posts',on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # the data that is created will be saved automatically
    created = models.DateTimeField(auto_now_add=True)
    # data is updated automatically
    updated = models.DateTimeField(auto_now=True)
    # status is only given from the parameters in STATUS_CHOICES
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    objects = models.Manager() # The default manager.
    published = PublishedManager() # custom manager.
    # published can now be used as manager eg Post.published.filter(title__startwith="Hello")

    def get_absolute_url(self):
           return reverse('blog:post_detail',
                          args=[self.publish.year,
                                self.publish.strftime('%m'),
                                self.publish.strftime('%d'),
                                self.slug])
    # sort the results by publish fields in descending order
    class Meta:
        ordering = ('-publish',)

    # it represents the objects as string - human readable
    def __str__(self):
        return self.title

    tags = TaggableManager()

class Comment(models.Model):
    # on_delete=models.CASCADE ==> When the referenced object is deleted, also delete the objects that have references to it
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {} '.format(self.name,self.post)






