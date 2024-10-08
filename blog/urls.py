## blog/urls.py
## description: the app-specific URLS for the blog application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name) format
    path(r'', views.RandomArticleView.as_view(), name="random"), 
    path(r'show_all_articles', views.ShowAllView.as_view(), name="show_all_articles"), 
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"), 
 
]