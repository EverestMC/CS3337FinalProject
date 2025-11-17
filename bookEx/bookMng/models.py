from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class MainMenu(models.Model):
    item = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)


class Comment(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  #newest first, got from Stack Overflow

    @property
    def author_title(self):
        return 'Admin' if self.author.is_staff else 'User'

    def __str__(self):
        return f'{self.author_title}: {self.author.username} on {self.book.name}'