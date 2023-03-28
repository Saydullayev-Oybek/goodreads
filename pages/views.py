from django.core.paginator import Paginator
from django.shortcuts import render
from book.models import BookReview
# Create your views here.

def home_page(request):
    book_reviews = BookReview.objects.all().order_by('-created_time')

    page_size = request.GET.get('page_size', 5)
    paginator = Paginator(book_reviews, page_size)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'home.html', context)