## hw/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name) format
    path(r'', views.quote, name="quote"), ## our first URL (index page)
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"), 
    path(r'about', views.about, name="about",)
]