from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'bookMng'

urlpatterns = [
    path('', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('book_comment/<int:book_id>/', views.book_comment, name='book_comment'),  # keep POST comment endpoint

    # NEW
    path('aboutus', views.aboutus, name='aboutus'),
    path('toggle_favorite/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)