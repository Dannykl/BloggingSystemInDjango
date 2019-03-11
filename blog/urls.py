"""bloging_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # post views
    path('',views.post_list, name='post_list'), # this is function based for list of posts
    # path('',views.PostListView.as_view(),name='post_list'), # this is classed based for list of posts
    path('tag/(?P<tag_slug>[-\w]+)/',views.post_list,name='post_list_by_tag'), # this is only used if tags is given to list post by tags
    path('(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/''(?P<post>[-\w]+)/',views.post_detail,name='post_detail'),
    path('(?P<post_id>\d+)/share/',views.post_share,name='post_share'),
]




# url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
    #         r'(?P<post>[-\w]+)/$',
    #         views.post_detail,
    #         name='post_detail'),
