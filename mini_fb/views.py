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


class CreateStatusMessageView(CreateView):
    ''' a view to show/process the CreateStatuseMessage form '''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        ''' pass the Profile object to the template '''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get( pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        ''' attach the Profile to the StatusMessage before saving '''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile 
        return super().form_valid(form)

    def get_success_url(self):
        ''' redirect back to the Profile page after successful submission '''
        return reverse('show_profile', kwargs=self.kwargs)