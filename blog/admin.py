from django.contrib import admin
from .models import Post,Comment
# Register your models here to include them into Django administration site.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')

admin.site.register(Comment,CommentAdmin)

# list_display to control which fields are displayed on the change list page of the admin.
# If you don’t set list_display, the admin site will display a single column that displays
# the __str__() representation of each object
# list_filter to activate filters in the right sidebar of the change list page of the admin
