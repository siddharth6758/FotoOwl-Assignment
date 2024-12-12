from django.urls import path
from books.views import *

urlpatterns = [
    path('book-details/<int:id>',BookView.as_view(),name='view-book'),
    path('manage-books',manage_books,name='manage-book'),
    path('book-add',BookView.as_view(),name='add-book'),
    path('book-update/<int:id>',BookView.as_view(),name='update-book'),
    path('book-delete/<int:id>',BookView.as_view(),name='delete-book')
]