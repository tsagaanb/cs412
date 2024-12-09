# project/admin.py

from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(BookProgress)
admin.site.register(Friendship)
admin.site.register(FriendRequest)

