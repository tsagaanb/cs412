# project/urls.py
# description: the app-specific URLS for the CS412 final project

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.ShowAllBooksView.as_view(), name='show_all_books'),
    path(r'book/<int:pk>/', views.ShowBookDetailsView.as_view(), name='show_book'),
    # path(r'login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    # path(r'logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),

]