from django.test import TestCase
from django.urls import reverse
from .models import Book


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



