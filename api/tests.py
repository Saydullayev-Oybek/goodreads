from rest_framework.test import APITestCase
from django.urls import reverse

from book.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPICase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='oybek',
            first_name='Oybek',
            last_name='saydullayev',
            email='oybek@gmail.com'
        )
        self.user.set_password('password')
        self.user.save()

    def test_review_detail(self):
        book = Book.objects.create(title='title1', description='description1', isbn='1231231')

        comment = BookReview.objects.create(user=self.user, book=book, stars_given=4, comment='this is comment')

        response = self.client.get(reverse('review_detail', kwargs={'id': book.id}))

        self.assertEqual(comment.comment, 'this is comment')
        self.assertEqual(comment.stars_given, 4)
        self.assertEqual(comment.book, book)
        self.assertEqual(comment.user, self.user)

    def test_book_reviews(self):
        book = Book.objects.create(title='title1', description='description1', isbn='1231231')
        user2 = CustomUser.objects.create(username='oybekking', email='oybekjohn@gmail.com')
        comment = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='this is good comment')
        comment2 = BookReview.objects.create(user=user2, book=book, stars_given=3, comment='this is bad comment')
        response = self.client.get(reverse('reviews'))

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], comment.id)
        self.assertEqual(response.data[0]['stars_given'], comment.stars_given)
        self.assertEqual(response.data[0]['comment'], comment.comment)
        self.assertEqual(response.data[1]['id'], comment2.id)
        self.assertEqual(response.data[1]['stars_given'], comment2.stars_given)
        self.assertEqual(response.data[1]['comment'], comment2.comment)


