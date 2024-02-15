from datetime import datetime
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import *
from fairy_tairy.permissions import *
from .serializers import *


class DiaryViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = DiarySerializer
    queryset = Diary.objects.all()
    
    def filter_queryset(self,queryset):
        queryset = queryset.filter(user = self.request.user)
        return super().filter_queryset(queryset)
    
    def create(self, request, *args, **kwargs):
        user_input_data = request.data
        
        # 다이어리 생성
        # comment생성, 연결
        # music생성, 연결
        # image 생성, 연결
        
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
class DiaryAdminViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsAdminUser]
    serializer_class = DiarySerializer
    queryset = Diary.objects.all()

        
class DiaryBookViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = DiarySerializer
    queryset = Diary.objects.all()
    
    def filter_queryset(self,queryset):
        queryset = queryset.filter(user = self.request.user)
        return super().filter_queryset(queryset)
    
    @action(detail=True, methods=['GET'])
    def get_book_diaries(self, request, pk = None):
        diary = self.get_object()
        book_diaries = Diary.objects.filter(book = diary.book, user = request.user)
        serializer = self.get_serializer(book_diaries, many = True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def connect_to_book(self, request, pk=None):
        diary = self.get_object()
        book_id = request.data.get('book_id')

        if not book_id:
            return Response({'detail': 'book_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, id=book_id, user=request.user)

        diary.book = book
        diary.save()

        serializer = self.get_serializer(diary)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def disconnect_book(self, request, pk=None):
        diary = self.get_object()

        # 연결을 해제하려면 해당 필드를 None으로 설정
        diary.book = None
        diary.save()

        serializer = self.get_serializer(diary)
        return Response(serializer.data)


class DiaryMusicViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
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
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def disconnect_music(self, request, pk=None):
        diary = self.get_object()

        # 연결을 해제하려면 해당 필드를 None으로 설정
        diary.music = None
        diary.save()

        serializer = self.get_serializer(diary)
        return Response(serializer.data)
    
