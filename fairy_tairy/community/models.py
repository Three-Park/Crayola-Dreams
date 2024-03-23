from django.db import models
from django.conf import settings
# Create your models here.

class FriendRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    friend = models.IntegerField()
    text = models.TextField(max_length = 50)
    
    request_send = models.BooleanField()
    requested_at = models.DateTimeField(auto_now=True)
    
    class Meta: 
        managed = True
        db_table = 'friend_requet'

class Friend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    friend = models.IntegerField()
    
    accepted_at = models.DateTimeField(auto_Now = True)
    
    class Meta: 
        managed = True
        db_table = 'friend'
