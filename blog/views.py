# blog/view.py
# views to show the blog application
from django.shortcuts import render

from . models import *
from django.views.generic import ListView
# Create your views here.

class ShowAllView(ListView):
    ''' A view to show all Articles '''
    
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

