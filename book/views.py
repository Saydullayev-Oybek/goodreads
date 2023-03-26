from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Book
from django.views import View


# class BooksListView(ListView):
#     model = Book
#     template_name = 'books/books_list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'

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


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    pk_url_kwarg = 'id'


# class BookDetailView(View):
#     def get(self, request, id):
#         book = Book.objects.get(id=id)
#         context = {
#             'book': book
#         }
#         return render(request, 'books/book_detail.html', context)

