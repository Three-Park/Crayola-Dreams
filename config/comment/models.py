from django.db import models
from diary.models import Diary
# Create your models here.
class Comment(models.Model):
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE)
    description = models.CharField(max_length = 100)