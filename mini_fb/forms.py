# mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    ''' A form to create a Profile data '''

    class Meta:
        ''' Associate this form with the Profile model '''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image']

class CreateStatusMessageForm(forms.ModelForm):
    ''' A form to create a Status Message for a profile '''

    class Meta:
        ''' Associate this form with the StatuseMessage model '''
        model = StatusMessage
        fields = ['message']