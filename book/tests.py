from django.test import TestCase
from django.urls import reverse
from .models import Book


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books_list'))

        self.assertContains(response, 'No books found.')

    def test_list_book(self):
        Book.objects.create(title='title1', description='description1', isbn='12342412')
        Book.objects.create(title='title2', description='description2', isbn='12342414')
        Book.objects.create(title='title3', description='description3', isbn='12342416')

        response = self.client.get(reverse('books_list'))

        books = Book.objects.all()
        for book in books:
            self.assertContains(response, book.title)

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

