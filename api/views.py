from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import BookReviewSerializer
from book.models import BookReview


class BookReviewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        book_review = BookReview.objects.get(id=id)

        serializer = BookReviewSerializer(book_review)

        return Response(data=serializer.data)


class ReviewsSerializer(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = BookReview.objects.all().order_by('-created_time')

        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(reviews, request)

        serializer = BookReviewSerializer(page_obj, many=True)

        return paginator.get_paginated_response(serializer.data)
