from django.urls import path
from .views import create_diary, diary_list, view_diary, edit_diary, delete_diary, django_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', create_diary, name='create_diary'),
    path('list/', diary_list, name='diary_list'),
    path('view/<int:pk>/', view_diary, name='view_diary'),
    path('edit/<int:pk>/', edit_diary, name='edit_diary'),
    path('delete/<int:pk>/', delete_diary, name='delete_diary'),
    path('django_view/', django_view, name='django_view'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)