from django.urls import path
from .views import (
    BooksListView,
    BookDetailView,
    BookReviewView,
    ReviewEditView,
    ReviewDeleteView,
    ReviewSuccessDelete,
    BookAuthorView
)

urlpatterns = [
    path('', BooksListView.as_view(), name='books_list'),
    path('<int:id>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:id>/review/', BookReviewView.as_view(), name='review'),
    path('<int:author_id>/book_author/', BookAuthorView.as_view(), name='book_author'),
    path('<int:book_id>/review/<int:comment_id>/edit/', ReviewEditView.as_view(), name='review_edit'),
    path('<int:book_id>/review/<int:comment_id>/delete/confirm', ReviewDeleteView.as_view(), name='confirm_review_delete'),
    path('<int:book_id>/review/<int:comment_id>/delete/', ReviewSuccessDelete.as_view(), name='review_delete')
]