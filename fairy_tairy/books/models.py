from django.db import models
from django.conf import settings
# Create your models here.

class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book_title = models.CharField(max_length = 30)
    author = models.CharField(max_length = 30)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        managed = True
        db_table = 'book'
