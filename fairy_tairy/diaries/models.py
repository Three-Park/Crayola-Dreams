from django.db import models
from django.conf import settings
from books.models import Book
from recommend_music.models import Music

class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.SET_NULL, blank=True, null=True)
    book = models.ForeignKey(Book,on_delete=models.SET_NULL, blank=True, null=True)
    
    title = models.CharField(max_length = 30)
    content = models.TextField()
    registered_at = models.DateTimeField(auto_now_add=True)
    last_update_at = models.DateTimeField(auto_now=True)
    
    class Meta: 
        managed = True
        db_table = 'diary'
