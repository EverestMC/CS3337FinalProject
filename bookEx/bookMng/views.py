from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import BookForm, CommentForm
from .models import MainMenu, Book, Comment

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


#Create your views here.
def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })


def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


def book_detail(request, book_id):
    #safer fetch + pic_path handling(from AI)
    book = get_object_or_404(Book, id=book_id)
    try:
        book.pic_path = book.picture.url[14:]
    except Exception:
        book.pic_path = ''

    #provide comments + empty form to the template
    comments = Comment.objects.filter(book=book)  #ordered via Meta(newest first)
    comment_form = CommentForm()

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'comments': comments,
                      'comment_form': comment_form,
                  })


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()

    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


#handle posting a new comment for a book (logged-in users only)
@login_required
def book_comment(request, book_id):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('book_detail', args=[book_id]))

    book = get_object_or_404(Book, id=book_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.book = book
        comment.author = request.user
        comment.save()

    #always redirect to avoid duplicate posts on refresh
    return HttpResponseRedirect(reverse('book_detail', args=[book_id]))
