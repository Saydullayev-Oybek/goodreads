from django.urls import path
# from .views import BookReviewDetail, ReviewsSerializer
from .views import BookReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('reviews', BookReviewViewSet, basename='review')
urlpatterns = router.urls


# urlpatterns = [
#     path('reviews/', ReviewsSerializer.as_view(), name='reviews'),
#     path('reviews/<int:id>/', BookReviewDetail.as_view(), name='review_detail')
# ]