# project/views.py
# views for the CS412 Final Project 

from . models import  *
from . forms import *

from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic import ListView, DetailView, CreateView, \
                                 UpdateView, DeleteView, View
from django.urls import reverse
from collections import defaultdict
from typing import Any
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import login 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm


class ShowAllBooksView(ListView):
    ''' A view to show a list of all the Books '''

    model = Book
    template_name = 'project/show_all_books.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = self.get_queryset()

        # Group books by genre
        genre_groups = defaultdict(list)
        for book in books:
            genre = book.classify_genre()
            genre_groups[genre].append(book)

        # Add the grouped books to the context
        context['genre_groups'] = dict(genre_groups)  # Convert defaultdict to a normal dict for the template
        return context

class ShowAllAuthorsView(ListView):
    ''' A view to show a list of all the Authors '''

    model = Author
    template_name = 'project/show_all_authors.html'
    context_object_name = 'authors'
    
    def get_queryset(self):
        # Order authors alphabetically by first name
        return Author.objects.all().order_by('author_first_name')

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
    
class CreateUserProfileView(CreateView):
    ''' A view to show/process the CreateUserProfile form '''

    form_class = CreateUserProfileForm
    template_name = 'project/create_user_profile_form.html'

class CreateReviewView(LoginRequiredMixin, CreateView):
    ''' A view to show/process the CreateReview form '''

    form_class = CreateReviewForm
    template_name = 'project/create_review_form.html'

class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    ''' A view to process the UpdateUserProfile form '''

    model = UserProfile
    form_class = UpdateProfileForm
    temlate_name = 'project/update_profile_form.html'


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    ''' A view to process the UpdateReview form '''

    model = Review
    form_class = UpdateReviewForm
    template_name = 'project/update_review_form.html'
    context_object_name = 'review'

class DeleteReviewView(LoginRequiredMixin, DeleteView):
    ''' A view to delete a review '''

    model = Review
    template_name = 'project/delete_review_form.html'
    context_object_name = 'review'

class CreateFriendshipView(LoginRequiredMixin, View):
    ''' A view to create a Friendship between two UserProfile objects '''

    def dispatch(self, request, *args, **kwargs):
        ''' creates a frienship using the add_friend method between the 
            current User and a different user '''

        user = self.request.user
        userProfile = UserProfile.objects.get(user = user)
        other_pk = self.kwargs.get('other_pk')
        other_UserProfile = UserProfile.objects.get(pk = other_pk)

        userProfile.add_friend(other_UserProfile)

        return redirect(reverse('show_profile', kwargs={'pk': userProfile.id}))
    
    def get_object(self):
        ''' find the profile related to the USER '''

        user = self.request.user
        userProfile = UserProfile.objects.get(user=user)

        return userProfile