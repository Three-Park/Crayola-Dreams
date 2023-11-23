from django.contrib import admin
from django.urls import include, path
from .views import main_page_view

urlpatterns = [
    path('', main_page_view, name='main_page'),
    path('admin/', admin.site.urls),
    path('diary/', include('diary.urls')),
    path('users/', include('users.urls')),
]
