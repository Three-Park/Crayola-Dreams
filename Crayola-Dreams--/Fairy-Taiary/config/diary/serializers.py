from rest_framework import serializers
from .models import Diary

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['user','title','content','image_url','registered_date','last_update_date']