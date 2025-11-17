from django import forms
from django.forms import ModelForm
from .models import Book, Comment


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]

class CommentForm(ModelForm):
    content = forms.CharField(
        label='Add a comment',
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'What did you think about the Book?'})
    )
    class Meta:
        model = Comment
        fields = ['content']