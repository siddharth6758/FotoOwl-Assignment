from django.shortcuts import render
from django.views import View
from books.models import Books
from library.models import LibraryManagement
from django.utils.timezone import now

class BookView(View):

    def get(self, request, id):
        book_obj = Books.objects.get(id=id)
        if LibraryManagement.objects.filter(
            book_borrowed__id=book_obj.id,
            borrow_on__lte=now(),
            borrow_till__gte=now()
        ).exists():
            book_available = False
        else:
            book_available = True
        context = {
            'book':book_obj,
            'book_available':book_available
        }
        return render(request,'book_detail.html',context)

def manage_books(request):
    books = Books.objects.all()
    context = {
        'books':books
    }
    return render(request,'book_manage.html',context=context)