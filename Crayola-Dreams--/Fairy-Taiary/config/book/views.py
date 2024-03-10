from django.shortcuts import render
from rest_framework import mixins, generics
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from config.config.permissions import IsOwner

class BookList(ListAPIView):
    queryset=Book.objects.all()
    print(queryset)
    serializer_class = BookCoverSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookDetail(generics.RetrieveAPIView):
    serializer_class = BookSerializer

    def retrieve(self, request, pk):
        model=Book.objects.get(pk=pk)
        serializer=self.get_serializer(model)
        return Response(serializer.data)


class DiaryToBook(generics.UpdateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        diary_ids = request.data.get('diaries', [])  # assuming that diaries are passed as a list of ids
        book.diaries.set(diary_ids)
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    


class BookViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    
    def filter_queryset(self,queryset):
        queryset = queryset.filter(user = self.request.user)
        return super().filter_queryset(queryset)
