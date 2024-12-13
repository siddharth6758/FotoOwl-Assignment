from django.shortcuts import render, redirect
from django.views import View
from library.models import LibraryManagement
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, StreamingHttpResponse
from books.models import Books
from django.utils.timezone import now
from datetime import timedelta
import csv

class Echo:
    def write(self, value):
        return value

echo_buffer = Echo()
writer = csv.writer(echo_buffer)

class LibraryManageView(View):

    def get(self, request, type):
        context = {}
        if type == 'borrow_history':
            borrow_history = LibraryManagement.objects.filter(
                request_status='completed'
            )
            context['borrow_history'] = borrow_history
            return render(request, 'borrow_history.html', context=context)
        elif type == 'borrow_request':
            borrow_request = LibraryManagement.objects.filter(
                request_status='pending'
            )
            context['borrow_requests'] = borrow_request
            return render(request, 'borrow_request.html', context=context)
        else:
            messages.error(request,'Invalid request type!')
            return redirect('user-homepage-url')

    def post(self, request, id):
        try:
            days = request.POST.get('borrow_days')
            if not days and days<1:
                messages.warning(request,f'Days cannot be less than 1!')
                return redirect(f'/book-borrow-request/{id}')
            book = Books.objects.get(id=id)
            calculated_days = now() + timedelta(days=int(days))
            LibraryManagement.objects.create(
                borrow_by=request.user,
                book_borrowed=book,
                borrow_till=calculated_days
            )
            messages.success(request,f'Request generated successfully!')
        except Exception as e:
            messages.error(request,f'Error {str(e)} while generating request!')
        return redirect('user-homepage-url')


@login_required
def get_book_borrow_page(request, id):
    book = Books.objects.get(id=id)
    context = {
        'book':book
    }
    return render(request,'book_request_page.html',context=context)

@csrf_exempt
def export_history_csv(request):
    try:
        queryset = LibraryManagement.objects.filter(request_status='completed')
        rows = []
        header_list = ["Book", "Requested By", "From", "To", "Answered By", "Is Approved"]
        rows.append(writer.writerow(header_list))
        for row in queryset:
            rows.append(writer.writerow([row.book_borrowed.title+' By '+row.book_borrowed.author, row.borrow_by, row.borrow_on.strftime('%d-%m-%Y %H:%M:%S'), row.borrow_till.strftime('%d-%m-%Y %H:%M:%S'), row.decision_by, row.is_approved]))
        filename = "Book_Borrow_History.csv"
        response = StreamingHttpResponse(rows, content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename='+filename
        return response
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=404)


@login_required(login_url='/login/')
def approve_disapprove_request(request, type, id):
    req_obj = LibraryManagement.objects.get(id=id)
    try:

        if type == 'approve':
            req_obj.is_approved = True
        elif type == 'disapprove':
            req_obj.is_approved = False

        req_obj.decision_by = request.user
        req_obj.request_status = 'completed'
        req_obj.save()
        messages.info(request,f'Request {type}d!')
    except Exception as e:
        messages.error(request,f'Error {str(e)} occured while processing request!')
    return redirect(f'/library-book/borrow_request')