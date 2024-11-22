# project/views.py
# views for the CS412 Final Project 

from django.shortcuts import render, redirect
from . models import  *
from django.views.generic import ListView, DetailView
from django.urls import reverse

class ShowAllBooksView(ListView):
    ''' A view to show a list of all the Books '''

    model = Book
    template_name = 'project/show_all_books.html'
    context_object_name = 'books'


class ShowAllAuthorsView(ListView):
    ''' A view to show a list of all the Authors '''

    model = Author
    template_name = 'project/show_all_authors.html'
    context_object_name = 'authors'


class ShowBookDetailsView(DetailView):
    ''' A view to show the details of one selected book '''
    
    model = Book
    template_name = 'project/show_book.html'
    context_object_name = 'book'


class ShowAuthorDetailsView(DetailView):
    ''' A view to show the details of one selected author '''

    model = Author
    template_name = 'project/show_author.html'
    context_object_name = 'author'
    