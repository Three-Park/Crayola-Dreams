from datetime import datetime
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from fairy_tairy.permissions import *
from ai.comment import get_comment
from .models import *
from .serializers import *

class EmotionViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsAuthenticated]
    serializer_class = EmotionSerializer
    queryset = Emotion.objects.all()
    
    def filter_queryset(self,queryset):
        queryset = queryset.filter(diary__user=self.request.user)
        return super().filter_queryset(queryset)
    
    def perform_create(self, serializer):
        diary_instance = serializer.validated_data['diary']
        chat = get_comment(diary_instance.content)
        serializer.save(chat=chat)
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        diary_instance = serializer.validated_data['diary']
        chat = get_comment(diary_instance.content)
        serializer.save(chat=chat)
        return super().perform_update(serializer)