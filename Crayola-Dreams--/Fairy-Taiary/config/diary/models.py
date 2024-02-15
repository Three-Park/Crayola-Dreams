from django.db import models
from django.conf import settings
# Create your models here.

class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length = 30)
    content = models.TextField()
    image_url = models.ImageField(upload_to='images/', default=None, blank=True, null=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    
    class Meta: 
        managed = True
        db_table = 'diary'
        app_label = 'diary' 
        