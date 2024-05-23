from django.db import models
from diaries.models import Diary

# Create your models here.
class Image(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True)
    image_prompt = models.TextField(null=True)
    class Meta:
        managed = True
        db_table = 'image'
