# project/models.py
# Data structures for the models in the CS412 Final Project

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    '''
    Model for the data attributes of individual users for our app
    '''
    # each user profile is asociated with a USER
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # data attributes:
    user_first_name = models.TextField(blank=False)
    user_last_name = models.TextField(blank=False)
    user_email = models.EmailField(unique=True)
    user_dob = models.DateField(blank=False)
    user_profile_pic = models.ImageField(blank=False)

    def __str__(self):
        ''' returns a string representation of the userprofile '''
        return f"{self.user_first_name} {self.user_last_name}"


class Author(models.Model):
    '''
    Model for the data attributes of Authors
    '''
    # data attributes:
    author_google_id = models.CharField(max_length=200, unique=True, blank=False)  # Unique ID for Google Books API
    author_first_name = models.TextField(blank=False)
    author_last_name = models.TextField(blank=False)
    author_birth_date = models.DateField(blank=True, null=True)  # Birth date
    author_death_date = models.DateField(blank=True, null=True)  # Death date
    author_biography = models.TextField(blank=True, null=True)

    def __str__(self):
        ''' returns a string representation of this author '''
        return f"{self.author_first_name} {self.author_last_name}"


class Book(models.Model):
    '''
    Model for the data attributes of Books
    '''
    # books are referenced to their Author
    book_author = models.ForeignKey('Author', on_delete=models.CASCADE)

    # data attributes:
    book_google_id = models.CharField(max_length=200, unique=True, blank=False)  # Unique ID for Google Books API
    book_title = models.TextField(blank=False)
    book_subtitle = models.TextField(blank=True, null=True)  
    book_categories = models.TextField(blank=True, null=True) 
    book_description = models.TextField(blank=True, null=True)
    book_publish_date = models.DateField(blank=True, null=True) 
    book_cover_image = models.URLField(blank=True, null=True)
    book_page_count = models.IntegerField(blank=True, null=True)
    book_languages = models.TextField(blank=True, null=True)

    def __str__(self):
        ''' returns a string representation of this book '''
        return f"{self.book_title} by {self.book_author}"


class Review(models.Model):
    '''
    Model for the data attributes of Reviews written by a user
    '''
    # the review must be referenced to a user
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    # a review is related to either a book or a movie
    book = models.ForeignKey('Book', on_delete=models.CASCADE, blank=True, null=True)

    # other data attributes:
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ''' returns a string representation of a book review written by a user '''
        return f"Review of {self.book.book_title} by {self.user.user_first_name}"


class BookProgress(models.Model):
    '''
    Model for the data attributes of a Book Progress of a user
    '''
    # the book progress must be referenced to a user
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    # the book progress must be referenced to a Book in the database
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    # other data attributes:
    status = models.CharField(max_length=50, choices=[('reading', 'Reading'), ('read', 'Read'), ('want to read', 'Want to Read')])
    rating = models.IntegerField(blank=True, null=True, choices=[(i, i) for i in range(1, 6)])  # 1-5 rating

    def __str__(self):
        ''' returns a string representation of the book progress for a user '''
        return f"book progress on {self.book.book_title} by {self.user.user_first_name}"

class Friendship(models.Model):
    '''
    Model for the friendship between two UserProfile objects
    '''
    # must refer to 2 UserProfile objects
    user1 = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='user2')

    anniversary = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ''' returns a string representation of a frienship between two users '''
        return f"{self.user1.user_first_name} {self.user1.user_last_name} & \
            {self.user2.user_first_name} {self.user2.user_last_name}"
