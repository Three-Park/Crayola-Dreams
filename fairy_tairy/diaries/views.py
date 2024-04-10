from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q

from .models import *
from books.models import *
from fairy_tairy.permissions import *
from .serializers import *


class DiaryViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsOwner]

    serializer_class = DiarySerializer
    queryset = Diary.objects.all()
    
    def filter_queryset(self,queryset):
        queryset = queryset.filter(user=self.request.user)
        return super().filter_queryset(queryset)
    
    # def get_queryset(self):
    #     user = self.request.user
    #     return Diary.objects.filter(Q(user=user))
    
    
class DiaryAdminViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsAdminUser]
    serializer_class = DiarySerializer
    queryset = Diary.objects.all()
    

class DiaryMusicViewSet(GenericViewSet,
                  mixins.ListModelMixin):
    permission_classes = [IsOwner,IsAuthenticated]
    serializer_class = DiaryMusicSerializer
    queryset = Diary.objects.all()
    
    def filter_queryset(self,queryset):
        queryset = queryset.filter(user = self.request.user)
        return super().filter_queryset(queryset)

    @action(detail=True, methods=['POST'])
    def connect_to_music(self, request, pk = None):
        diary = self.get_object()
        music_id = request.data.get('music_id')

        if not music_id:
            return Response({'detail': 'music_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        music = get_object_or_404(Music, id=music_id, user=request.user)

        diary.music = music
        diary.save()

        serializer = self.get_serializer(diary)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'])
    def disconnect_music(self, request, pk=None):
        diary = self.get_object()

        # 연결을 해제하려면 해당 필드를 None으로 설정
        diary.music = None
        diary.save()

        serializer = self.get_serializer(diary)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
