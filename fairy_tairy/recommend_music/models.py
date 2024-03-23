from django.db import models

# Create your models here.
class Music(models.Model):
    music_title = models.CharField(max_length=50)
    artist = models.CharField(max_length=100)
    music_url = models.URLField()
    
    class Meta:
        managed = True
        db_table = 'music'