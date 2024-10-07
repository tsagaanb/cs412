# mini_fb/models.py

from django.db import models

class Profile(models.Model):
    ''' 
    Model for the data attributes of individual Facebook user profiles.
    '''

    # data attributes:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)


# make migrations only when you modify the data attibutes
    def __str__(self):
        ''' Return a string represntation of this profile '''
        return f"{self.first_name} {self.last_name}"


    
