from django.urls import path
from django.conf import settings
from .views import BookList,BookCreate,BookView


urlpatterns = [
    path('list/', BookList.as_view(), name='book_list'),
    path('view/<int:pk>/', BookView.as_view(), name='view_book'),
    path('create/',BookCreate.as_view(), name='create_book')

]
