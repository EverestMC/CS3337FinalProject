from django.contrib import admin
from .models import MainMenu, Book, Comment, Rating

admin.site.register(MainMenu)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Rating)
