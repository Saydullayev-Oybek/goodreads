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

        self.client.login(username='oybek', password='password')

    def test_review_detail(self):
        book = Book.objects.create(title='title1', description='description1', isbn='1231231')

        comment = BookReview.objects.create(user=self.user, book=book, stars_given=4, comment='this is comment')

        response = self.client.get(reverse('review-detail', kwargs={'id': comment.id}))

        self.assertEqual(comment.comment, 'this is comment')
        self.assertEqual(comment.stars_given, 4)
        self.assertEqual(comment.book, book)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['book']['id'], book.id)
        self.assertEqual(response.data['book']['title'], book.title)

    def test_book_reviews(self):
        book = Book.objects.create(title='title1', description='description1', isbn='1231231')
        user2 = CustomUser.objects.create(username='oybekking', email='oybekjohn@gmail.com')
        comment = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='this is good comment')
        comment2 = BookReview.objects.create(user=user2, book=book, stars_given=3, comment='this is bad comment')

        response = self.client.get(reverse('review-list'))

        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['stars_given'], comment2.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], comment2.comment)
        self.assertEqual(response.data['results'][1]['id'], comment.id)
        self.assertEqual(response.data['results'][1]['stars_given'], comment.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], comment.comment)
        self.assertEqual(response.data['results'][0]['id'], comment2.id)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_create_book_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='234324')

        response = self.client.post(reverse('review-list'), data={
            'stars_given': 4,
            'comment': 'comment',
            'user_id': self.user.id,
            'book_id': book.id
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['comment'], 'comment')
        self.assertEqual(response.data['stars_given'], 4)

    def test_delete_book_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='234324')
        book_review = BookReview.objects.create(stars_given=4, comment='good', book=book, user=self.user)

        response = self.client.delete(reverse('review-detail', kwargs={'id': book_review.id}))

        self.assertEqual(response.status_code, 204)

    def test_patch_book_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='234324')
        book_review = BookReview.objects.create(stars_given=4, comment='good', book=book, user=self.user)

        response = self.client.patch(reverse('review-detail', kwargs={'id': book_review.id}), data={
            'stars_given': 5,
            'comment': 'bad'
        })
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 5)
        self.assertEqual(book_review.comment, 'bad')

    def test_put_book_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='234324')
        book_review = BookReview.objects.create(stars_given=4, comment='good', book=book, user=self.user)

        response = self.client.put(reverse('review-detail', kwargs={'id': book_review.id}), data={
            'user_id': self.user.id,
            'book_id': book.id,
            'stars_given': 3,
            'comment': 'this is bad comment'
        })
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 3)
        self.assertEqual(book_review.comment, 'this is bad comment')


        response = self.client.put(reverse('review-detail', kwargs={'id': book_review.id}), data={
            'book_id': book.id,
            'stars_given': 3,
            'comment': 'this is bad comment'
        })
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 400)