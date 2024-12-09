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
        labels = {
            'user_first_name': 'First Name',
            'user_last_name': 'Last Name',
            'user_email': 'Email Address',
            'user_dob': 'Date of Birth YYYY-MM-DD',
            'user_profile_pic': 'Profile Picture',
        }

    def __init__(self, *args, **kwargs):
        ''' Method that overrides the __init__ method to add custom behavior to the form when initiliazed '''

        super().__init__(*args, **kwargs)

        # Add placeholders for each field
        self.fields['user_first_name'].widget.attrs.update({
            'placeholder': 'e.g., John'
        })
        self.fields['user_last_name'].widget.attrs.update({
            'placeholder': 'e.g., Doe'
        })
        self.fields['user_email'].widget.attrs.update({
            'placeholder': 'e.g., john.doe@example.com'
        })
        self.fields['user_dob'].widget.attrs.update({
            'placeholder': 'e.g., 1990-01-01'
        })
        self.fields['user_profile_pic'].widget.attrs.update({
            'placeholder': 'Choose a profile picture (optional)'
        })
        # Add consistent form styling (optional)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class CreateReviewForm(forms.ModelForm):
    ''' A form to create a Review data '''

    class Meta:
        ''' Associate this form with the Review model '''
        model = Review
        fields = ['book', 'rating', 'content']


class UpdateUserProfileForm(forms.ModelForm):
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
    
