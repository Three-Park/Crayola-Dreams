from django.urls import path
from . import views

urlpatterns = [
    path('gen_comment/<int:diary_id>/', views.gen_comment, name='gen_comment'),
]