# blog/forms.py

from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    ''' A form to create Comment data. '''

    class Meta:
        ''' Associate this form with the Commend model '''
        model = Comment
        fields = ['author', 'text', ]  # which fields from model should we use

