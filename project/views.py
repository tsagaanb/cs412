# project/views.py
# views for the CS412 Final Project 

from django.shortcuts import render, redirect
from . models import  *
from django.views.generic import ListView, DetailView
from django.urls import reverse
from collections import defaultdict


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
    
# class CreateUserProfileView(CreateView):
#     ''' A view to show/process the CreateUserProfile form '''

#     form_class = CreateUserProfileForm
#     template_name = 'project/create_user_profile_form.html'

# class CreateReviewView(LoginRequiredMixin, CreateView):
#     ''' A view to show/process the CreateReview form '''

#     form_class = CreateReviewForm
#     template_name = 'project/create_review_form.html'

# class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
#     ''' A view to process the UpdateUserProfile form '''

#     model = UserProfile
#     form_class = UpdateProfileForm
#     temlate_name = 'project/update_profile_form.html'


# class UpdateReviewView(LoginRequiredMixin, UpdateView):
#     ''' A view to process the UpdateReview form '''

#     model = Review
#     form_class = UpdateReviewForm
#     template_name = 'project/update_review_form.html'
#     context_object_name = 'review'

# class DeleteReviewView(LoginRequiredMidin, DeleteView):

#     ''' A view to delete a review '''
#     model = Review
#     template_name = 'project/delete_review_form.html'
#     context_object_name = 'review'

# class CreateFriendshipView(View):
#     ''' A view to create a Friendship between two UserProfile objects '''


