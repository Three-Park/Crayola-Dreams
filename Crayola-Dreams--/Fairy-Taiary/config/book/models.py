from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from diary.models import Diary

class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book_title = models.CharField(max_length = 30)
    author = models.CharField(max_length = 30)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        managed = True
        db_table = 'book'

class Page(models.Model):
    book_id=models.ForeignKey('Book', on_delete=models.CASCADE)
    diary_id=models.ForeignKey('diary.Diary', on_delete=models.CASCADE)
    page_num=models.IntegerField(blank=True,null=True)

    class Meta:
        db_table='pages'