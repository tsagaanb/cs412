# mini_fb/models.py

from django.db import models
from django.urls import reverse


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
        status_message = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return status_message

    def get_friends(self):
        ''' Return all the friends of a Profile object in a list '''
        friends_profile1 = Friend.objects.filter(profile1=self)
        friends_profile2 = Friend.objects.filter(profile2=self)

        friends = []
        # If the current profile is profile1:
        for friend in friends_profile1:
            friends.append(friend.profile2)

         # If the current profile is profile2:
        for friend in friends_profile2:
            friends.append(friend.profile1)

        return friends

    def add_friend(self, other):
        ''' A method that takes a parameter other, which referes to another
            Profile and adds a Friend relation for the 2 Profiles '''
        if self == other:
            raise ValueError("A profile cannot friend itself.")
        
        existing_friend = Friend.objects.filter(profile1=self, profile2=other) | \
                            Friend.objects.filter(profile1=other, profile2=self)
        if existing_friend:
            print("Friend relationship already exists.")
        else:
            friend = Friend()
            friend.profile1 = self
            friend.profile2 = other
            friend.save()

    def get_friend_suggestions(self):
        ''' Returns a list of possible friends for a Profile '''        
        # Get the friends that already exist
        existing_friends = self.get_friends()
        friends_pks = []
        for friend in existing_friends:
            friends_pks.append(friend.pk)

        suggestions = []
        all_profiles = Profile.objects.all()

        # Exclude the current profile and existing friends from the list of all profiles
        for profile in all_profiles:
            if ((profile != self) and (profile not in existing_friends)):
                suggestions.append(profile)
        
        return suggestions
        
    
    def get_news_feed(self):
        ''' Returns the status messages and images associated to a 
            Profile and and that of their friends '''

        pks = []
        # Add the pk of the profile itself
        pks.append(self.pk)

        friends = self.get_friends()
        # Add the pks of the friends
        for friend in friends:
            pks.append(friend.pk)
        # Filter the statusmessages for everyone associated with the profile
        news_feed = StatusMessage.objects.filter(profile__pk__in=pks).order_by('-timestamp')

        return news_feed


    def get_absolute_url(self):
        ''' Return the Profile '''
        return reverse('show_profile', kwargs={'pk': self.id})


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
        
    def get_images(self):
        ''' Return the image related to the StatusMessage object '''
        image = Image.objects.filter(status_message=self)
        return image
    

class Image(models.Model):
    ''' 
    Model for the data attributes of the Image related to a single StatusMessage
    '''

    image = models.ImageField(blank=True)
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    '''
    Model for the frienship of two Profile objects
    '''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    anniversary = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ''' Return a string representation of the friendship between 2 profiles '''
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"



