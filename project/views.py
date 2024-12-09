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

# imports used for language selection
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def set_language(request):
    ''' View to set the user's preferred language in the session '''
    if request.method == 'POST':
        language = request.POST.get('language', 'all')  # Default to All Books
        request.session['language'] = language
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the previous page

def get_books(request):
    ''' Returns books based on the selected language or show all books by default '''

    selected_language = request.session.get('language', 'all')  # Default to showing all books if no language is selected
    if selected_language and selected_language != 'all':
        books = Book.objects.filter(book_languages=selected_language)
    else:
        books = Book.objects.all()  # Show all books when 'All Books' is selected or no language is set
    return books


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

        # pass the User Profile to display the link to their profile on the NAV BAR
        user_profile = None
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=self.request.user).first()
        context['user_profile'] = user_profile

        return context

    def get_queryset(self):
        # Use the get_books function to get books based on language
        return get_books(self.request)


class ShowAllAuthorsView(ListView):
    ''' A view to show a list of all the Authors '''

    model = Author
    template_name = 'project/show_all_authors.html'
    context_object_name = 'authors'

    def get_queryset(self):
        # Get the selected language from the session
        selected_language = self.request.session.get('language', 'all')  # Default to "all"
        
        if selected_language == 'all' or not selected_language:
            # Return all authors if "All Books" is selected
            authors = Author.objects.all().order_by('author_first_name')
        else:
            # Filter authors who have books in the selected language
            authors = Author.objects.filter(book__book_languages=selected_language).distinct().order_by('author_first_name')

        return authors

    def get_context_data(self):
        # pass the User Profile to display the link to their profile on the NAV BAR
        user_profile = None
        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=self.request.user).first()
        context['user_profile'] = user_profile


class ShowBookDetailsView(DetailView):
    ''' A view to show the details of one selected book '''
    
    model = Book
    template_name = 'project/show_book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated: 
            user_profile = UserProfile.objects.get(user = self.request.user)
            context['user_profile'] = user_profile

            # book progress (for add to shelf feature)
            book_progress = BookProgress.objects.filter(user=user_profile, book=book).first()
            default_shelf = book_progress if book_progress else None
            context['book_progress'] = default_shelf

            # section to get if any of the user's friends shelved this book
            # Retrieve the user's friends
            friends = user_profile.get_friends()

            # Filter BookProgress for the friends and the current book
            friends_progress = BookProgress.objects.filter(book=book, user__in=friends)

            context['friends_progress'] = friends_progress

        return context

class ShowAuthorDetailsView(DetailView):
    ''' A view to show the details of one selected author '''

    model = Author
    template_name = 'project/show_author.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use the get_books function and filter further by author
        all_books = get_books(self.request)
        context['books'] = all_books.filter(book_author=self.object).order_by('book_publish_date')

        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated: 
            user_profile = UserProfile.objects.get(user = self.request.user)
            context['user_profile'] = user_profile

        return context
    
class ShowAllUserProfileView(ListView):
    ''' A view to show the list of all the users '''
    model = UserProfile
    template_name = 'project/show_all_users.html'
    context_object_name = 'profile'

    def get_context_data(self):
         # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        
        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated: 
            user_profile = UserProfile.objects.get(user = self.request.user)
            context['user_profile'] = user_profile

        return context


class ShowUserProfileView(DetailView):
    ''' A view to show the profile of a user '''
    model = UserProfile
    template_name = 'project/show_user_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
         # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        
        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated: 
            user_profile = UserProfile.objects.get(user = self.request.user)
            context['user_profile'] = user_profile

        # get the books that the user is READING/WANT TO READ/READ
        user_profile = self.get_object()
        context['currently_reading'] = BookProgress.objects.filter(user=user_profile, status='reading')
        context['want_to_read'] = BookProgress.objects.filter(user=user_profile, status='want to read')
        context['read_books'] = BookProgress.objects.filter(user=user_profile, status='read')
        return context


    def get_object(self, queryset=None):
        ''' Ensure we fetch the correct user profile based on the pk '''
        pk = self.kwargs.get('pk')
        return UserProfile.objects.get(pk=pk)


    def get_absolute_url(self):
        ''' Returns the Profile ''' 
        return reverse('show_user_profile', kwargs={'pk': self.id})

class CreateUserProfileView(CreateView):
    ''' A view to show/process the CreateUserProfile form '''

    form_class = CreateUserProfileForm
    template_name = 'project/create_user_profile_form.html'

    def get_success_url(self):
        ''' displays the UserProfile model '''
        return self.object.get_absolute_url()

    def get_login_url(self):
        ''' return the URL required for login '''
        return reverse('login')

class CreateBookProgressView(LoginRequiredMixin, CreateView):
    ''' A view to create a BookProgress for a user '''

    def dispatch(self, request, *args, **kwargs):
        # get the logged in user
        user = self.request.user
        # get the user_profile instance of the logged in user
        user_profile = UserProfile.objects.get(user = user)

        # get the book that the user is trying to shelve
        book_pk = self.kwargs.get('book_pk')
        book = Book.objects.get(pk=book_pk)

        # Get the progress status from the request (e.g., "reading", "read", "want to read")
        status = self.request.POST.get('status')

        # Check if status is provided
        if not status:
            return redirect(reverse('show_book', kwargs={'pk': book_pk}))

        # Create or update the BookProgress
        book_progress, created = BookProgress.objects.get_or_create(
            user=user_profile,
            book=book,
            defaults={'status': status}
        )
        if not created:
            book_progress.status = status
            book_progress.save()

        # Redirect back to the book detail page or profile page
        return redirect(reverse('show_user_profile' , kwargs={'pk': user_profile.pk }))

class DeleteBookProgressView(LoginRequiredMixin, DeleteView):
    ''' A view to delete a BookProgress '''
    model = BookProgress
    context_object_name = 'book_progress'

    def get_success_url(self):
        ''' redirect back to the book detail page '''
        return reverse('show_book', kwargs={'pk': self.object.book.pk})

    def get_queryset(self):
        ''' Restricts deletion to the logged-in user's BookProgress instances '''
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        return BookProgress.objects.filter(user=user_profile)
        

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