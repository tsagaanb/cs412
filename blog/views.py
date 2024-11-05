# blog/view.py
# views to show the blog application
from django.shortcuts import render

from . models import *
from . forms import *
from django.views.generic import ListView, DetailView, CreateView
from typing import Any
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login 
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


import random
# Create your views here.

class ShowAllView(ListView):
    ''' A view to show all Articles '''
    
    model = Article
    template_name = 'blog/show_all_articles.html'
    context_object_name = 'articles'

    def dispatch(self, *args, **kwargs):
        '''
        implement this method to add some tracing
        '''
        print(f"self.request.user={self.request.user}")
        # delegate to superclass version
        return super().dispatch(*args, **kwargs)


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

class CreateCommentView(LoginRequiredMixin, CreateView):
    ''' a view to show/process the create comment form:
    on GET: sends back the form
    on POST: read the form data, create and instance of Comment; save to database '''

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


class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to create a new Article and save it to the database.'''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        ''' Add some debuggin statements '''
        print(f'CreateArticleView.form_valid: form.cleaned_data={form.cleaned_data}')

        # find which user user logged in
        user = self.request.user
        print(f'CreateArticleView:form_valid() user:{user}')
        # attach the user to hte new article instance
        form.instance.user = user
        # delegate work to superclass
        return super().form_valid(form)

    def get_login_url(self) -> str:
        ''' return the URL required for login '''
        return reverse('blog_login')


class RegistrationView(CreateView):
    ''' Handle registration of new Users '''

    template_name = 'blog/register.html'
    form_class = UserCreationForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        '''Handle the User creation form submission '''

        # If we received an HTTP POST, we handle it
        if self.request.POST:
            print(f"RegistrationView.dispatch: self.request.POST={self.request.POST}")

            # reconstruct the UserCreateForm ffrom the POST data
            form = UserCreationForm(self.request.POST)
            if not form.is_valid():
                print(f"form.errors={form.errors}")
                return super().dispatch(request, *args, **kwargs)

            # save the form, which creates a new User
            user = form.save() # this will commit the insert to the database
            print(f"RegistrationView.dispatch: created user {user}")
            # log the User in  
            login(self.request, user)
            print(f"RegistrationView.dispatch: {user} is logged in")

            # note for mini_fb: attach the FK user to the Profile form instance

            # return a response
            return redirect(reverse('show_all_articles'))


        # Let CreateView.dispatch handle the HTTP GET Request
        return super().dispatch(request, *args, **kwargs)