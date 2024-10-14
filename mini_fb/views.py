# mini_fb/views.py
# views to show the mini_fb application
from django.shortcuts import render

from . models import *
from . forms import *
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse


# Create your views here.

class ShowAllProfilesView(ListView):
    ''' A view to show all the Profiles '''
    
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    ''' Show one selected profile '''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile' 

class CreateProfileView(CreateView):
    ''' a view to show/process the Create Profile form'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self):
        ''' displays the Profile model '''
        return self.object.get_absolute_url()

