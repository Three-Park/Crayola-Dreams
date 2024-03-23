from datetime import datetime
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import *
from fairy_tairy.permissions import *
from .serializers import *


class FriendRequestViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequest
    queryset = FriendRequest.objects.all()
    
    def filter_queryset(self,queryset):
        queryset = queryset.filter(user = self.request.user)
        return super().filter_queryset(queryset)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
    
    
class FriendViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = FriendRequest
    queryset = FriendRequest.objects.all()
    
    def filter_queryset(self,queryset):
        queryset = queryset.filter(user = self.request.user)
        return super().filter_queryset(queryset)