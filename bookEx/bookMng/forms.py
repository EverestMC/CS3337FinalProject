from django import forms
from django.forms import ModelForm
from .models import Book, Comment, Rating


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'web', 'price', 'picture']


class RatingForm(forms.Form):
    # Simple radio style; render as stars in the template
    score = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect
    )


class CommentForm(ModelForm):
    content = forms.CharField(
        label='',
        max_length=500,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Write your comment here',
            'style': 'width:100%; padding:8px; border-radius:6px; border:1px solid #ccc;'
        })
    )

    class Meta:
        model = Comment
        fields = ['content']
