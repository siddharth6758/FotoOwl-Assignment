from django.urls import path
from books.views import *

urlpatterns = [
    path('book-details/<int:id>',BookView.as_view(http_method_names=['get']),name='view-book'),
    path('manage-books',manage_books,name='manage-book'),
    path('add-books',add_books,name='add-book-page'),
    path('book-add',BookView.as_view(http_method_names=['post']),name='add-book'),
    path('book-update/<int:id>',BookUpdateView.as_view(http_method_names=['post']),name='update-book'),
    path('book-delete/<int:id>',BookUpdateView.as_view(http_method_names=['get']),name='delete-book')
]