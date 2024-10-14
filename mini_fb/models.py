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
    profile_image = models.URLField(blank=True)


# make migrations only when you modify the data attibutes
    def __str__(self):
        ''' Return a string represntation of this profile '''
        return f"{self.first_name} {self.last_name}"
    def get_status_messages(self):
        '''Return all of the status messages for this profile.'''
        status_message = StatusMessage.objects.filter(profile=self)
        return status_message


class StatusMessage(models.Model):
    '''
    Model for the data attributes of Facebook status message
    '''

    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this Facebook Status object.'''
        return f'{self.message}'
    
