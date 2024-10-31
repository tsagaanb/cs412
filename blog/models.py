# blog/models.py
# Define data models (objects) for use in the blog application
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    ''' 
    Encapsulate the data for a blog Article by some author.
    '''
    # Each article will be associated with a User
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    # data attributes:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)



# make migrations only when you modify the data attibutes
    def __str__(self):
        ''' Return a string represntation of this Article '''
        return f"{self.title} by {self.author}"

    def get_comments(self):
        '''Return all of the comments about this article.'''
        comments = Comment.objects.filter(article=self)
        return comments

    def get_absolute_url(self):
        ''' Return the URL to view one instance of this object'''
        # self.pk is the primary key for an object instance
        pk = self.pk
        return reverse('article', kwargs={'pk': pk} )



class Comment(models.Model):
    '''Encapsulate the idea of a Comment on an Article.'''
    
    # data attributes of a Comment:
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'