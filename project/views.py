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
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import login 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm

# imports used for language selection
from django.views.decorators.csrf import csrf_exempt

# FOR SEARCH ENGINE
# to find fuzzy matches for the search query from a list of book titles or author names.
from difflib import get_close_matches
# to dynamically build queries to filter the database for those fuzzy matches.
from django.db.models import Q

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


def fuzzy_filter_books(queryset, field, query):
    ''' Filter books by partial and fuzzy matching on title '''
    # Partial matching using icontains
    partial_matches = queryset.filter(book_title__icontains=query)

    # Fuzzy matching using difflib
    field_values = queryset.values_list("book_title", flat=True)
    close_matches = get_close_matches(query.lower(), [title.lower() for title in field_values], n=10, cutoff=0.6)

    # Combine both sets of matches
    return queryset.filter(
        Q(book_title__in=close_matches) | Q(book_title__icontains=query)
    )


def fuzzy_filter_authors(queryset, fields, query, cutoff=0.6):
    """Filter authors by partial and fuzzy matching on multiple fields."""
    # Partial matching using icontains
    partial_matches = queryset.filter(
        Q(author_first_name__icontains=query) | Q(author_last_name__icontains=query)
    ).distinct()  # Apply distinct here

    # Fuzzy matching using difflib
    field_values = {
        obj.pk: " ".join([str(getattr(obj, field, '')).lower() for field in fields])
        for obj in queryset
    }
    matches = get_close_matches(query.lower(), field_values.values(), cutoff=cutoff)
    matching_pks = [pk for pk, value in field_values.items() if value in matches]
    fuzzy_matches = queryset.filter(pk__in=matching_pks).distinct()  # Apply distinct here

    # Combine partial and fuzzy matches
    combined_queryset = partial_matches.union(fuzzy_matches, all=True)  # Do not apply distinct here
    return combined_queryset

# VIEWS START HERE
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
        query = self.request.GET.get('q', '')  # Get the search query

        # Use the get_books function to get books based on language
        books = get_books(self.request)  

        if query:
            # Filter books based on title or author name with fuzzy matching
            books = fuzzy_filter_books(books, 'book_title', query)

        return books


class ShowAllAuthorsView(ListView):
    ''' A view to show a list of all the Authors '''

    model = Author
    template_name = 'project/show_all_authors.html'
    context_object_name = 'authors'

    def get_queryset(self):
        # Get the selected language from the session
        selected_language = self.request.session.get('language', 'all')  # Default to "all"

        if selected_language == 'all' or not selected_language:
            authors = Author.objects.all()
        else:
            # Filter authors who have books in the selected language
            authors = Author.objects.filter(book__book_languages=selected_language).distinct()

        # Get the search query
        query = self.request.GET.get('q', '')

        if query:
            # Apply fuzzy filtering to match both first and last names
            authors = fuzzy_filter_authors(authors, ['author_first_name', 'author_last_name'], query)

        # Apply ordering after filtering
        return authors.order_by('author_first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # pass the User Profile to display the link to their profile on the NAV BAR
        user_profile = None
        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=self.request.user).first()
        context['user_profile'] = user_profile

        return context 

class ShowBookDetailsView(DetailView):
    ''' A view to show the details of one selected book '''
    
    model = Book
    template_name = 'project/show_book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user_profile = None

        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated: 
            user_profile = UserProfile.objects.get(user = self.request.user)

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

            # Get the user's review for this book
            try:
                user_review = Review.objects.get(book=book, user=user_profile)
                context['user_review'] = user_review
            except Review.DoesNotExist:
                context['user_review'] = None  # Set to None if no review exists

            # Add friends' reviews for the book
            friends_review =  Review.objects.filter(book=book, user__in=friends)
            if friends_review: 
                context['friends_reviews'] = friends_review

        context['user_profile'] = user_profile
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
        user_profile = None
        if self.request.user.is_authenticated: 
            user_profile = UserProfile.objects.get(user = self.request.user)
        context['user_profile'] = user_profile

        return context
    
class ShowAllUserProfileView(ListView):
    ''' A view to show the list of all the users '''
    model = UserProfile
    template_name = 'project/show_all_users.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated: 
            user_profile = UserProfile.objects.get(user = self.request.user)
            context['user_profile'] = user_profile
            context['other_profiles'] = context['profiles']

            # Add friend status for each profile in the queryset
            friends_list = user_profile.get_friends()  # Returns a list of friends
            for profile in context['other_profiles']:
                profile.is_friend = profile in friends_list
                profile.has_sent_request = FriendRequest.objects.filter(sender=user_profile, receiver=profile).exists()
                profile.has_received_request = FriendRequest.objects.filter(sender=profile, receiver=user_profile).exists()


        return context


class CreateFriendRequestView(LoginRequiredMixin, View):
    ''' A view to send a friend request to a different user '''

    def post(self, request, *args, **kwargs):
        sender = UserProfile.objects.get(user=request.user)
        receiver = UserProfile.objects.get(pk=kwargs['pk'])

        # Check if the friend request already exists
        if not FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            FriendRequest.objects.create(sender=sender, receiver=receiver)

        return redirect('show_all_users')


class ShowFriendRequestsView(LoginRequiredMixin, ListView):
    ''' A view to show the friends requests that a user has '''
    model = FriendRequest
    template_name = 'project/friend_requests.html'
    context_object_name = 'friends_requests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_profile = None
        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated:
            user = self.request.user
            user_profile = UserProfile.objects.get(user=user)
            context['user_profile'] = user_profile

            # Get pending friend requests sent to the logged-in user
            context['friend_requests'] = FriendRequest.objects.filter(receiver=user_profile, status='pending')
        
        return context


class AcceptFriendRequestView(LoginRequiredMixin, View):
    ''' A view to accept a friend request '''

    def post(self, request, *args, **kwargs):
        friend_request_id = self.kwargs.get('request_id')
        friend_request = FriendRequest.objects.get(id=friend_request_id)

        # Check if the logged-in user is the receiver of the friend request
        if friend_request.receiver.user == request.user:
            # Create a friendship
            Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)

            # Delete the friend request object
            friend_request.delete()

        return redirect('friend_requests')


class RejectFriendRequestView(LoginRequiredMixin, View):
    ''' A view to reject a friend request '''

    def post(self, request, *args, **kwargs):
        friend_request_id = self.kwargs.get('request_id')
        friend_request = FriendRequest.objects.get(id=friend_request_id)

        # Check if the logged-in user is the receiver of the friend request
        if friend_request.receiver.user == request.user:
            # Delete the friend request object
            friend_request.delete()

        return redirect('friend_requests')

class ShowUserProfileView(LoginRequiredMixin, DetailView):
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

            # Determine the viewed profile
            viewed_profile = self.get_object()
            is_own_profile = user_profile == viewed_profile
            context['is_own_profile'] = is_own_profile

            if not is_own_profile:
                # Check friendship status
                friends_list = user_profile.get_friends()
                context['is_friend'] = viewed_profile in friends_list

                # Check if a friend request has been sent by the logged-in user
                context['has_sent_request'] = FriendRequest.objects.filter(
                    sender=user_profile, receiver=viewed_profile).exists()

                # Check if a friend request exists FROM the viewed profile TO the logged-in user
                received_request = FriendRequest.objects.filter(
                    sender=viewed_profile, receiver=user_profile).first()
                context['has_received_request'] = received_request is not None
                context['received_request_id'] = received_request.id if received_request else None

                # Determine if a friend request can be sent
                context['can_send_request'] = not context['is_friend'] and not context['has_sent_request']

            # Add reviews to context if the profile is the logged-in user's or a friend's
            if is_own_profile or context.get('is_friend', False):
                context['reviews'] = Review.objects.filter(user=viewed_profile)


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

    def get_login_url(self) -> str:
        ''' return the URL required for login '''
        return reverse('login')

    def form_valid(self, form):
        ''' process both forms if valid '''
        # reconstruct the UserCreateForm ffrom the POST data
        user_form = UserCreationForm(self.request.POST)
        
        # check if both forms are valid
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            # automatically log the user in after registration
            login(self.request, user)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ''' add UserCreationForm to the context '''
        context = super().get_context_data(**kwargs)
        user_form = UserCreationForm
        context['user_form'] = user_form
        return context

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
    model = Review
    form_class = CreateReviewForm
    template_name = 'project/create_review_form.html'

    def get_object(self):
        ''' find the profile related to the USER '''
        user = self.request.user
        profile = UserProfile.objects.get(user = user)
        
        return profile

    def form_valid(self, form):
        # Automatically assign the user and book to the review
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)

        book_pk = self.kwargs.get('book_pk')
        book = Book.objects.get(pk=book_pk)

        # Redirect to the update review page if a review already exists
        existing_review = Review.objects.filter(book=book, user=user_profile).first()

        if existing_review:
            return HttpResponseRedirect(reverse('update_review', args=[existing_review.pk]))

        form.instance.user = user_profile
        form.instance.book = book  # Use the book set in dispatch
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get the logged in user 
        user = self.request.user
        user_profile = UserProfile.objects.get(user = user)
        context['user_profile'] = user_profile

        book_pk = self.kwargs.get('book_pk')
        book = Book.objects.get(pk=book_pk)

        context['book'] = book # Pass the book object to the template
        return context

    def get_success_url(self, **kwargs):
        # Redirect to the book detail page after the review is created
        book_pk = self.kwargs.get('book_pk')

        return reverse('show_book', kwargs={'pk': book_pk})


class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    ''' A view to process the UpdateUserProfile form '''

    model = UserProfile
    form_class = UpdateUserProfileForm
    template_name = 'project/update_profile_form.html'

    def get_object(self):
        ''' find the profile related to the USER '''
        user = self.request.user
        user_profile = UserProfile.objects.get(user = user)
        
        return user_profile

    def get_success_url(self):
        ''' redirect back to the Profile page after successful update '''
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        return reverse('show_user_profile', kwargs={'pk': user_profile.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # pass the User Profile to display the link to their profile on the NAV BAR
        user_profile = None
        # find the user who is logged in and make sure that they are autenticated
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=self.request.user).first()
        context['user_profile'] = user_profile

        return context 

class UpdateReviewView(LoginRequiredMixin, UpdateView):
    ''' A view to process the UpdateReview form '''

    model = Review
    form_class = UpdateReviewForm
    template_name = 'project/update_review_form.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        ''' Pass the book related to the review into the context '''
        # get the logged in user 
        user = self.request.user
        user_profile = UserProfile.objects.get(user = user)
        context['user_profile'] = user_profile

        context = super().get_context_data(**kwargs)
        context['book'] = self.object.book
        return context

    def get_success_url(self):
        ''' redirect back to the Profile page after successful deletion '''
        review_pk = self.kwargs.get('pk')
        review = Review.objects.get(pk=review_pk)
        book = review.book
        return reverse('show_book', kwargs={'pk': book.pk})
       

class DeleteReviewView(LoginRequiredMixin, DeleteView):
    ''' A view to delete a review '''

    model = Review
    template_name = 'project/delete_review_form.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        ''' Pass the book related to the review into the context '''
        context = super().get_context_data(**kwargs)
        # get the logged in user 
        user = self.request.user
        user_profile = UserProfile.objects.get(user = user)
        context['user_profile'] = user_profile

        # get the book that the review is for
        context['book'] = self.object.book
        return context

    def get_success_url(self):
        ''' redirect back to the Profile page after successful deletion '''
        review_pk = self.kwargs.get('pk')
        review = Review.objects.get(pk=review_pk)
        book = review.book
        return reverse('show_book', kwargs={'pk': book.pk})
       

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