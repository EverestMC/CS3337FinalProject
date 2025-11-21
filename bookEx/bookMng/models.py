from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.utils import timezone


class MainMenu(models.Model):
    item = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # NEW: favorites toggle
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # ----- Rating helpers (NEW) -----
    def average_rating(self):
        agg = Rating.objects.filter(book=self).aggregate(avg=Avg('score'))
        return agg['avg'] or None

    def rating_count(self):
        return Rating.objects.filter(book=self).count()

    def user_rating(self, user):
        if not user or not user.is_authenticated:
            return None
        r = Rating.objects.filter(book=self, user=user).first()
        return r.score if r else None


class Comment(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    @property
    def author_title(self):
        return 'Admin' if self.author.is_staff else 'User'

    def __str__(self):
        return f'{self.author_title}: {self.author.username} on {self.book.name}'


# NEW: 1–5 star rating by user per book (unique per user+book)
class Rating(models.Model):
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=SCORE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.book} - {self.score} by {self.user.username}"
