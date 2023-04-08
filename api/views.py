from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import BookReviewSerializer
from book.models import BookReview


class BookReviewDetail(APIView):
    def get(self, request, id):
        book_review = BookReview.objects.get(id=id)

        serializer = BookReviewSerializer(book_review)

        return Response(data=serializer.data)


class ReviewsSerializer(APIView):
    def get(self, request):
        reviews = BookReview.objects.all()

        serializer = BookReviewSerializer(reviews, many=True)

        return Response(data=serializer.data)
