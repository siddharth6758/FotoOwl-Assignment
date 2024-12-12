from django.shortcuts import render, redirect
from django.views import View
from books.models import Books
from library.models import LibraryManagement
from django.utils.timezone import now
from django.contrib import messages

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

    def post(self, request):
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        cover_image = request.FILES.get('cover_image')

        try:
            Books.objects.create(
                title=title,
                author=author,
                description=description,
                cover_image=cover_image
            )
            messages.success(request,f'Successfully Created!')
        except Exception as e:
            print(f'Exception occured during Creating Book | error: {str(e)}')
            messages.error(request,f'Error while creating: {str(e)}!')
        return redirect('manage-book')

class BookUpdateView(View):

    def post(self, request, id):
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        cover_image = request.FILES.get('cover_image')

        try:
            book = Books.objects.get(id=id)
            book.title=title
            book.description=description
            book.author=author
            if cover_image:
                book.cover_image=cover_image
            book.save()
            messages.success(request,f'Successfully Updated!')
        except Exception as e:
            print(f'Exception occured during Updating Book: {Books.object.get(id=id).title}, Error: {str(e)}')
            messages.error(request,f'Error while updating: {str(e)}!')
        return redirect(f'/book-details/{id}')


def manage_books(request):
    books = Books.objects.all()
    context = {
        'books':books
    }
    return render(request,'book_manage.html',context=context)


def add_books(request):
    return render(request,'book_add.html')