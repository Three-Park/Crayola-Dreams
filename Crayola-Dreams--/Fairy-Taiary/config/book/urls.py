from django.urls import path
from .views import *

urlpatterns = [
    path('list/', BookList.as_view(), name='list_book'),
    path('view/',BookDetail.as_view(),name='view_book'),
    path('create/',DiaryToBook.as_view(),name='edit_book'),
]