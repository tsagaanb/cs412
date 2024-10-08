# blog/view.py
# views to show the blog application
from django.shortcuts import render

from . models import *
from django.views.generic import ListView, DetailView
import random
# Create your views here.

class ShowAllView(ListView):
    ''' A view to show all Articles '''
    
    model = Article
    template_name = 'blog/show_all_articles.html'
    context_object_name = 'articles'


class RandomArticleView(DetailView):
    ''' Show one article selected at random '''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article' # note the singular 
    
    def get_object(self):
        ''' Return the instance of the Article object to show.'''
        # get all articles
        all_articles = Article.objects.all()
        # pick one at random
        random_article = random.choice(all_articles)
        return random_article

class ArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html' ## reusing same template!!
    context_object_name = 'article'