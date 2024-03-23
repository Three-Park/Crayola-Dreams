from rest_framework import serializers
from diaries.serializers import DiarySerializer
from .models import *


class EmotionSerializer(serializers.ModelSerializer):
    diary = DiarySerializer()
    class Meta:
        model = Emotion
        fields = '__all__'

