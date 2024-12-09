# project/forms.py

from django import forms
from .models import UserProfile, Review, BookProgress

# unfriend hiih option oruulahu yahu?

class CreateUserProfileForm(forms.ModelForm):
    ''' A form to create a UserProfile data '''

    class Meta:
        ''' Associate this form with the UserProfile model '''
        model = UserProfile
        fields = ['user_first_name', 'user_last_name', 'user_email', 'user_dob', 'user_profile_pic']


class CreateReviewForm(forms.ModelForm):
    ''' A form to create a Review data '''

    class Meta:
        ''' Associate this form with the Review model '''
        model = Review
        fields = ['book', 'rating', 'content']


class UpdateProfileForm(forms.ModelForm):
    ''' A form to update an existing UserProfile object '''

    class Meta:
        ''' Associate this form with the UserProfile model '''
        model = UserProfile
        fields = ['user_email', 'user_profile_pic']

class UpdateReviewForm(forms.ModelForm):
    ''' A form to update an existing Review object '''

    class Meta:
        ''' Associate this form with the Review model '''
        model = Review
        fields = ['rating', 'content']
    
