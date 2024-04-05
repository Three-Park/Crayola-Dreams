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
    
    permission_classes = [IsFollowerOrOwner]

    serializer_class = DiarySerializer
    queryset = Diary.objects.all()
    
    def get_queryset(self):
        """
        본인의 diary는 모두 보임, 친구의 diary는 is_open=true인 경우만 보이도록 필터링
        """
        user = self.request.user
        followed_users_1 = Follow.objects.filter(follower=user, status='accepted').values_list('following_user', flat=True)
        followed_users_2 = Follow.objects.filter(following_user=user, status='accepted').values_list('follower', flat=True)
        
        return Diary.objects.filter(Q(user=user) |
                                    Q(user__in=followed_users_1, is_open=True) | 
                                    Q(user__in=followed_users_2, is_open=True))
    
    
class DiaryAdminViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsAdminUser]
    serializer_class = DiarySerializer
    queryset = Diary.objects.all()

# class DiaryBookViewSet(GenericViewSet,
#                   mixins.ListModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin):
    
#     permission_classes = [IsOwner, IsAuthenticated]
#     serializer_class = DiarySerializer
#     queryset = Diary.objects.all()
    
#     def filter_queryset(self,queryset):
#         queryset = queryset.filter(user = self.request.user)
#         return super().filter_queryset(queryset)
    
#     @action(detail=True, methods=['GET'])
#     def get_book_diaries(self, request, pk = None):
#         diary = self.get_object()
#         book_diaries = Diary.objects.filter(book = diary.book, user = request.user)
#         serializer = self.get_serializer(book_diaries, many = True)
#         return Response(serializer.data)
    
#     @action(detail=True, methods=['POST'])
#     def connect_to_book(self, request, pk=None):
#         diary = self.get_object()
#         book_id = request.data.get('book_id')

#         if not book_id:
#             return Response({'detail': 'book_id is required'}, status=status.HTTP_400_BAD_REQUEST)

#         book = get_object_or_404(Book, id=book_id, user=request.user)

#         diary.book = book
#         diary.save()

#         serializer = self.get_serializer(diary)
#         return Response(serializer.data)

#     @action(detail=True, methods=['POST'])
#     def disconnect_book(self, request, pk=None):
#         diary = self.get_object()

#         # 연결을 해제하려면 해당 필드를 None으로 설정
#         diary.book = None
#         diary.save()

#         serializer = self.get_serializer(diary)
#         return Response(serializer.data)


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
    
