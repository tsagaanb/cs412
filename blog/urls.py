## blog/urls.py
## description: the app-specific URLS for the blog application

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views # user login, authentication
from . import views

# create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name) format
    path(r'', views.RandomArticleView.as_view(), name="random"), 
    path(r'show_all_articles', views.ShowAllView.as_view(), name="show_all_articles"), 
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"), 
    # path(r'create_comment', views.CreateCommentView.as_view(), name="create_comment"), 
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name="create_comment"),
    path(r'create_article', views.CreateArticleView.as_view(), name='create_article'),

    # authentication URLS:
    path(r'login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='blog_login'),
    path(r'logout/', auth_views.LogoutView.as_view(next_page='show_all_articles'), name='blog_logout'),
    path(r'register/', views.RegistrationView.as_view(), name='register'),

]