from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, BookReview
from django.views import View
from .forms import BookReviewForm


class BooksListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')

        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)

        paginator = Paginator(books, 2)
        page_num = request.GET.get('page', 1)

        page_obj = paginator.get_page(page_num)

        context = {
            'page_obj': page_obj,
            'search_query': search_query
        }
        return render(request, 'books/books_list.html', context)


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)

        comments = BookReview.objects.filter(book=book)

        book_review_form = BookReviewForm()

        context = {
            'book': book,
            'comments': comments,
            'book_review_form': book_review_form
        }
        return render(request, 'books/book_detail.html', context)



class BookReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book_review_form = BookReviewForm(data=request.POST)
        book = Book.objects.get(id=id)

        if book_review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                comment=book_review_form.cleaned_data['comment'],
                stars_given=book_review_form.cleaned_data['stars_given']
            )

            return redirect(reverse('book_detail', kwargs={'id': book.id}))

        return render(request, 'books/book_detail.html', {'book_review_form': book_review_form})


class ReviewEditView(LoginRequiredMixin, View):
    def get(self, request, book_id, comment_id):
        book = Book.objects.get(id=book_id)
        reviews = BookReview.objects.get(id=comment_id)
        review_form = BookReviewForm(instance=reviews)

        return render(request, 'books/review_edit.html', {'book': book, 'reviews': reviews, 'review_form': review_form})

    def post(self, request, book_id, comment_id):
        book = Book.objects.get(id=book_id)
        reviews = BookReview.objects.get(id=comment_id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            review_form.save()

            return redirect(reverse('book_detail', kwargs={'id': book_id}))

        return render(request, 'books/review_edit.html', {'book': book, 'reviews': reviews, 'review_form': review_form})


class ReviewDeleteView(LoginRequiredMixin, View):
    def get(self, request, book_id, comment_id):
        book = Book.objects.get(id=book_id)
        reviews = BookReview.objects.get(id=comment_id)

        context = {
            'book': book,
            'review': reviews
        }

        return render(request, 'books/review_delete.html', context)

class ReviewSuccessDelete(LoginRequiredMixin, View):
    def get(self, request, book_id, comment_id):
        review = BookReview.objects.get(id=comment_id)

        review.delete()
        messages.success(request, 'You have success delete comment')

        return redirect(reverse('book_detail', kwargs={'id': book_id}))