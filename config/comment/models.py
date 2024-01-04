from django.db import models

# Create your models here.
class Comment(models.Model):
    diary = models.ForeignKey("diary.Diary",on_delete=models.CASCADE)
    description = models.CharField(max_length = 100)