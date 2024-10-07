# mini_fb/views.py
# views to show the blog application
from django.shortcuts import render

from . models import *
from django.views.generic import ListView
# Create your views here.

class ShowAllProfilesView(ListView):
    ''' A view to show all the Profiles '''
    
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

