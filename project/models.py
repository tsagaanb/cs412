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
        ''' Returns a string representation of the userprofile '''
        return f"{self.user_first_name} {self.user_last_name}"

    def get_friends(self):
        ''' Returns all the frienships that exist with this User '''
        
        # find all the frienships that the user is involved with
        # user can either be user1 or user2
        friendships1 = Friendship.objects.filter(user1=self)
        friendships2 = Frienship.objects.filter(user2=self)

        friends = []
        # if the user was user1:
        for friendship in friendships1:
            friends.append(friendship.user2)

        # if the user was user2:
        for frienship in frienships2:
            friends.append(friendship.user1)

        return friends

    def add_friend(self, other):
        ''' A method that takes a parameter other, which refers to anotherr
            UserProfile object and adds a Frienship between the 2 UserProfiles '''

        # if user is trying to friend themselves
        if self == other:
            raise ValueError("A profile can't friend itself.")

        # Check if self and other are already friends 
        existing_friend = Friendship.objects.filter(user1=self, user2=other) | \
                            Friendship.object.fitler(user1=other, user2=self)

        if existing_friend:
            print("Friendship already exists!")

        # create frienship if not already friends
        else:
            friendship = Friendship()
            friendship.user1 = self
            friendship.user2 = other
            friendship.save()



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
        ''' Returns a string representation of this author '''
        return f"{self.author_first_name} {self.author_last_name}"

    def get_books(self):
        ''' Returns all the books written by the specified author '''
        books = Book.objects.filter(book_author = self).order_by('book_publish_date')
        return books


# Used for dividing all the books to different genres that they belong in 
GENRE_GROUPS = {
    "Fiction": ["general", "novel", "literature", "fiction", "contemporary", "historical fiction", "drama", "adventure", "mythology","magical realism"],
    "Non-Fiction": ["biography", "memoir", "history", "self-help", "non-fiction", "autobiography", "essays", "journalism", "politics", "philosophy", "economics", "psychology", "sociology", "travel", "education", "science", "true crime"],
    "Mystery & Thriller": ["mystery", "thriller", "crime", "suspense", "detective", "whodunit", "spy", "noir", "legal thriller"],
    "Science Fiction & Fantasy": ["science fiction", "fantasy", "dystopian", "space", "cyberpunk", "time travel", "post-apocalyptic", "steampunk", "high fantasy", "dark fantasy", "superheroes", "aliens", "epic fantasy"],
    "Romance": ["romance", "love", "romantic", "chick-lit", "historical romance", "erotica", "young adult romance", "young adult romance", "young adult romance"],
    "Horror": ["horror", "scary", "paranormal", "gothic","vampires", "ghosts", "ghost stories", "psychological horror", "slasher", "zombies", "demons"],
    "Children's Books": ["children", "kids", "juvenile", "middle grade", "picture books", "young adult", "nursery rhymes", "fairy tales", "board books"],
    "Lifestyle": ["health", "dating", "work-out", "health and wellness", "parenting", "self-improvement", "personal development", "mindfulness", "productivity", "wellness", "cooking"],
    "Technology": ["technology", "computer", "artificial intelligence", "data science", "computer science", "coding", "robotics", "software engineering"],
    "History": ["history", "ancient history", "military history", "world war", "medieval", "modern history", "cultural history"],
    "Literature": ["literature", "classic literature", "poetry", "literary fiction", "short stories", "contemporary literature", "plays"],
    "Art": ["painting", "drawing", "sculpture", "photography", "visual arts", "modern art", "art history", "digital art"],
    "Others": []  # Catch-all for unmatched categories
}

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
        ''' Returns a string representation of this book '''
        return f"{self.book_title} by {self.book_author}"

    def classify_genre(self):
        """
        Classify the book into one of the predefined genres based on book_categories.
        """
        categories = (self.book_categories or "").lower()  # Convert to lowercase for comparison
        for genre, keywords in GENRE_GROUPS.items():
            for keyword in keywords:
                if keyword in categories:
                    return genre
        return "Others"  # Default to "Others" if no match is found


class Review(models.Model):
    '''
    Model for the data attributes of Reviews written by a user
    '''
    # the review must be referenced to a user
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    # a review is related to either a book or a movie
    book = models.ForeignKey('Book', on_delete=models.CASCADE, blank=True, null=True)

    # other data attributes:
    rating = models.IntegerField(blank=True, null=True, choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ''' Returns a string representation of a book review written by a user '''
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
        ''' Returns a string representation of the book progress for a user '''
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
        ''' Returns a string representation of a frienship between two users '''
        return f"{self.user1.user_first_name} {self.user1.user_last_name} & \
            {self.user2.user_first_name} {self.user2.user_last_name}"
