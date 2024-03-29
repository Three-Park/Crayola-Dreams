from django.db import models
from diaries.models import Diary

# Create your models here.
class Emotion(models.Model):
    diary = models.ForeignKey(Diary,on_delete=models.DO_NOTHING)
    emotion_label = models.CharField(max_length = 10)
    name = models.CharField(max_length=30)
    emotion_prompt = models.TextField()
    chat = models.TextField()
    class Meta:
        db_table ='emotion' 