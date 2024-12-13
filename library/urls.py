from django.urls import path
from library.views import *

urlpatterns = [
    path('library-book/<str:type>',LibraryManageView.as_view(),name='library-get'),
    path('book-borrow-request/<int:id>',get_book_borrow_page,name='library-book-borrow-add'),
    path('library-book-borrow/<int:id>',LibraryManageView.as_view(),name='add-borrow-request'),
    path('ajax/download-history-csv',export_history_csv,name='borrow-history-csv'),
    path('approve-disapprove/<str:type>/<int:id>',approve_disapprove_request,name='approve-disapprove'),
]