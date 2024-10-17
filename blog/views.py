# blog/view.py
# views to show the blog application
from django.shortcuts import render

from . models import *
from . forms import *
from django.views.generic import ListView, DetailView, CreateView
from typing import Any
from django.urls import reverse

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
    context_object_name = 'article' # note the singular naming

class CreateCommentView(CreateView):
    ''' a view to show/process the create comment form:
    on GET: sends back the form
    on PSOT: read the form data, create and instance of Comment; save to database '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    # what to do after form submission?
    def get_success_url(self) -> str:
        # return '/blog/show_all_articles'
        # return reverse("show_all_articles")
        # above 2 do the same thing. One just uses the name instead of the url

        return reverse("article", kwargs=self.kwargs)

    def form_valid(self, form):
        ''' this method executes after the form submission '''

        print(f"CreateCommentView.form_valid(): form={form.cleaned_data}")
        print(f"CreateCommentView.form_valid(): self.kwargs={self.kwargs}")

        # find the article with the PK form the URL
        # self.kwargs['pk'] is finding the article PK form the URL
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attach the article to the comment
        # (form.instance is the new Comment object)
        form.instance.article = article

        # delegate work to the supserclass version of this methof
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the template context data --
            a dict of key-value pairs '''

        # get the super class version of context data
        context = super().get_context_data(**kwargs)

        # find the article with the PK form the URL
        # self.kwargs['pk'] is finding the article PK form the URL
        article = Article.objects.get(pk=self.kwargs['pk'])

        # add the article to the context data
        context['article'] = article 
        return context


class CreateArticleView(CreateView):
    '''A view to create a new Article and save it to the database.'''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        ''' Add some debuggin statements '''
        print(f'CreateArticleView.form_valid: form.cleaned_data={form.cleaned_data}')

        # delegate work to superclass
        return super().form_valid(form)
