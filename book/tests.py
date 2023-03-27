from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from .models import Book, BookReview


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books_list'))

        self.assertContains(response, 'No books found.')

    def test_list_book(self):
        book1 = Book.objects.create(title='title1', description='description1', isbn='12342412')
        book2 = Book.objects.create(title='title2', description='description2', isbn='12342414')
        book3 = Book.objects.create(title='title3', description='description3', isbn='12342416')

        response = self.client.get(reverse('books_list'))

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        response1 = self.client.get(reverse('books_list') + '?page=2')
        self.assertContains(response1, book3.title)

    def test_book_attributes(self):
        Book.objects.create(title='title', description='description', isbn='123245')
        books = Book.objects.all()

        for book in books:
            self.assertEqual(book.title, 'title')

    def test_book_detail(self):
        book = Book.objects.create(title='title', description='description', isbn='124124124')

        response = self.client.get(reverse('book_detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)


class BookPaginatorCase(TestCase):
    def test_has_next_page(self):
        book1 = Book.objects.create(title='title1', description='description1', isbn='234234324')
        book2 = Book.objects.create(title='title2', description='description2', isbn='234234325')
        book3 = Book.objects.create(title='title23', description='description23', isbn='2342343253')

        response = self.client.get(reverse('books_list') + '?page=2')
        self.assertContains(response, book3.title)


class BookSearchCase(TestCase):
    def test_search_book(self):
        book1 = Book.objects.create(title='title1', description='description1', isbn='234234324')
        book2 = Book.objects.create(title='title2', description='description2', isbn='234234325')
        book3 = Book.objects.create(title='title3', description='description23', isbn='2342343253')

        response = self.client.get(reverse('books_list') + '?q=title1')

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse('books_list') + '?q=title2')

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse('books_list') + '?q=title3')

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)


class BookReviewCase(TestCase):
    def test_add_book_review(self):
        book = Book.objects.create(title='title1', description='description1', isbn='234234324')
        user = CustomUser.objects.create(
            username='oybek',
            first_name='Oybek',
            last_name='saydullayev',
            email='oybek@gmail.com'
        )
        user.set_password('password')
        user.save()

        self.client.login(username='oybek', password='password')

        self.client.post(reverse('review', kwargs={'id': book.id}), data={
                'stars_given': 4,
                'comment': 'this is comment'
            }
        )

        book_reviews = BookReview.objects.filter(book=book)

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].comment, 'this is comment')
        self.assertEqual(book_reviews[0].stars_given, 4)
        self.assertEqual(book_reviews[0].user, user)
        self.assertEqual(book_reviews[0].book, book)



