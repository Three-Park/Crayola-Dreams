from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import generics, status, mixins, viewsets
from .serializers import BookSerializer,BookCoverSerializer,PageSerializer
from diary.serializers import DiarySerializer
from .models import Book,Page,Diary
from .forms import BookForm,PageForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from typing_extensions import Text

import io
import os
from django.conf import settings


class BookList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    queryset=Book.objects.all()
    serializer_class = BookCoverSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request,*args,**kwargs)
    



class BookView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               generics.GenericAPIView):
    queryset=Page.objects.all()
    serializer_class=PageSerializer

    def get(self, request, book_id):
        model=Page.objects.get(book_id)
        serializer=PageSerializer(model)

        pages=Page.objects.filter(book_id=book_id)
        diaries=[page.diary_id for page in pages]
        serializer=DiarySerializer(diaries,many=True)

        return Response(serializer.data)

#중간테이블 만들어서 하기
#중간테이블 showup만 하면 될듯

    
    
class BookCreate(mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset=Diary.objects.all()
    serializer_class = DiarySerializer
 
    def post(self, request, *args, **kwargs):
        queryset=Page.objects.all()
        serializer_class=BookSerializer

        diary_ids = request.data.get('diary_id', [])
        book_title = request.data.get('title')
        author = request.data.get('author')
        description = request.data.get('description',' ')
        
        # 새로운 Book 객체 생성
        book = Book.objects.create(
            book_title=book_title,
            author=author,
            description=description,
            user=request.user  # 현재 사용자
        )
        
        # 선택한 다이어리들을 새로운 Book에 추가
        for diary_id in diary_ids:
            Page.objects.create(book_id=book.id, diary_id=diary_id)
        
        return Response({"message": "Book created successfully"}, status=status.HTTP_201_CREATED)



    

    