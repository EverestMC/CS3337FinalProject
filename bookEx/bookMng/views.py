from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import MainMenu, Book, Comment, Rating
from .forms import BookForm, CommentForm, RatingForm

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


def index(request):
    return render(request, 'bookMng/index.html', {
        'item_list': MainMenu.objects.all()
    })


@login_required
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'bookMng/postbook.html', {
                'item_list': MainMenu.objects.all(),
                'form': BookForm(),
                'submitted': True
            })
    else:
        form = BookForm()

    return render(request, 'bookMng/postbook.html', {
        'item_list': MainMenu.objects.all(),
        'form': form,
        'submitted': False
    })


def displaybooks(request):
    books = Book.objects.all()

    # Attach picture URL and rating aggregates for UI
    for b in books:
        b.pic_url = b.picture.url if b.picture else ""
        b.avg_rating = b.average_rating()
        b.rating_count = b.rating_count()
        b.user_rating = b.user_rating(request.user) if request.user.is_authenticated else None

    return render(request, 'bookMng/displaybooks.html', {
        'item_list': MainMenu.objects.all(),
        'books': books,
        'showing_favorites': False
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # Rating submission
        if not request.user.is_authenticated:
            return redirect('login')

        form = RatingForm(request.POST)
        if form.is_valid():
            score = int(form.cleaned_data['score'])
            Rating.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'score': score}
            )
            return HttpResponseRedirect(request.path)
    else:
        form = RatingForm()
        if request.user.is_authenticated:
            existing = book.user_rating(request.user)
            if existing:
                form = RatingForm(initial={'score': existing})

    context = {
        'item_list': MainMenu.objects.all(),
        'book': book,
        'form': form,
        'avg_rating': book.average_rating(),
        'rating_count': book.rating_count(),
        'user_rating': book.user_rating(request.user) if request.user.is_authenticated else None,
        'comments': book.comments.all(),
        'comment_form': CommentForm(),
    }
    return render(request, 'bookMng/book_detail.html', context)


@login_required
def book_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                book=book,
                author=request.user,
                content=form.cleaned_data['content']
            )
    return redirect('bookMng:book_detail', book_id=book.id)


@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.is_favorite = not book.is_favorite
    book.save()
    # Prefer to return to where the user came from; fallback to list
    next_url = request.META.get('HTTP_REFERER') or reverse('bookMng:displaybooks')
    return redirect(next_url)


@login_required
def favorites(request):
    books = Book.objects.filter(is_favorite=True)
    for b in books:
        b.pic_url = b.picture.url if b.picture else ""
        b.avg_rating = b.average_rating()
        b.rating_count = b.rating_count()
        b.user_rating = b.user_rating(request.user)

    return render(request, 'bookMng/displaybooks.html', {
        'item_list': MainMenu.objects.all(),
        'books': books,
        'showing_favorites': True
    })


def mybooks(request):
    # Keep whatever filtering you already had here; leaving basic render
    return render(request, 'bookMng/mybooks.html', {
        'item_list': MainMenu.objects.all()
    })


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('bookMng:displaybooks')
    return render(request, 'bookMng/book_delete.html', {
        'item_list': MainMenu.objects.all(),
        'book': book
    })


def aboutus(request):
    return render(request, 'bookMng/aboutus.html', {
        'item_list': MainMenu.objects.all()
    })


# Optional: registration view if you use it
class Register(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
