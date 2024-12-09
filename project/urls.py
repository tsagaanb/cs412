# project/urls.py
# description: the app-specific URLS for the CS412 final project

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'set-language/', views.set_language, name='set_language'),
    path(r'', views.ShowAllBooksView.as_view(), name='show_all_books'),
    path(r'book/<int:pk>/', views.ShowBookDetailsView.as_view(), name='show_book'),

    path(r'authors/', views.ShowAllAuthorsView.as_view(), name='show_all_authors'),
    path(r'authors/<int:pk>/', views.ShowAuthorDetailsView.as_view(), name='show_author'),

    path(r'profile/<int:pk>/', views.ShowUserProfileView.as_view(), name='show_user_profile'),
    path(r'profile/update/', views.UpdateUserProfileView.as_view(), name='update_user_profile'),
    path(r'create_user_profile/', views.CreateUserProfileView.as_view(), name='create_user_profile'),
    path(r'users/', views.ShowAllUserProfileView.as_view(), name='show_all_users'),

    path(r'send_friend_request/<int:pk>/', views.CreateFriendRequestView.as_view(), name='send_friend_request'),
    path(r'friend_requests/', views.ShowFriendRequestsView.as_view(), name='friend_requests'),
    path(r'accept_friend_request/<int:request_id>/', views.AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path(r'reject_friend_request/<int:request_id>/', views.RejectFriendRequestView.as_view(), name='reject_friend_request'),

    path(r'book/<int:book_pk>/add_progress/', views.CreateBookProgressView.as_view(), name='add_book_progress'),
    path(r'book_progress/<int:pk>/delete/', views.DeleteBookProgressView.as_view(), name='delete_book_progress'),

    path(r'login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
]