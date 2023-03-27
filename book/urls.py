from django.urls import path
from .views import BooksListView, BookDetailView, BookReviewView
urlpatterns = [
    path('', BooksListView.as_view(), name='books_list'),
    path('<int:id>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:id>/review/', BookReviewView.as_view(), name='review')
]