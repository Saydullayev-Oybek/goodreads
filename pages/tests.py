from django.test import TestCase
from django.urls import reverse

from book.models import Book, BookReview
from users.models import CustomUser


class BookReviewsCase(TestCase):
    def test_book_add_review(self):
        book = Book.objects.create(title='title', description='description', isbn='123123')

        user = CustomUser.objects.create(
            username='oybek',
            first_name='Oybek',
            last_name='Saydulleyev',
            email='oybek@gmail.com',
        )
        user.set_password('password')

        review1 = BookReview.objects.create(user=user, book=book, stars_given=4, comment='comment1')
        review2 = BookReview.objects.create(user=user, book=book, stars_given=3, comment='comment3')
        review3 = BookReview.objects.create(user=user, book=book, stars_given='2', comment='comment4')

        response = self.client.get(reverse('home') + '?page_size=2')

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
