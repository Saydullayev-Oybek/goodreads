from django.urls import path
from .views import BookReviewDetail, ReviewsSerializer

urlpatterns = [
    path('reviews/', ReviewsSerializer.as_view(), name='reviews'),
    path('review/<int:id>/', BookReviewDetail.as_view(), name='review_detail')
]