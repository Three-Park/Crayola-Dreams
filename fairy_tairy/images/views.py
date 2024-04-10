# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# import boto3
# import urllib.parse
# from .forms import ImageForm
# from botocore.exceptions import NoCredentialsError
# import fairy_tairy.settings as settingss
# from ai.generate_image import *

# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             # 이미지를 S3에 업로드
#             image = form.cleaned_data['image']
#             upload_to_s3(image, settingss.AWS_STORAGE_BUCKET_NAME,'images/')

#             # 폼을 저장하여 모델에 이미지 정보 추가
#             image_instance = form.save(commit=False)
            
#             # S3에 업로드된 이미지의 URL 생성
#             file_name = urllib.parse.quote(image.name)
#             image_instance.image_url = f"https://{settingss.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/images/{file_name}"
            
#             image_instance.save()

#             return HttpResponse('Upload Successful')

#     else:
#         form = ImageForm()

#     return render(request, 'upload_image.html', {'form': form})

# def upload_to_s3(encoded_image):
#     s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

#     try:
#         image_data = base64.b64decode(encoded_image)
#         # image = Image.open(io.BytesIO(image_data))
#         image_key = 'images/{}.png'.format(uuid.uuid4())  # 이미지 파일명을 랜덤하게 생성
        
#         # 이미지를 S3에 업로드
#         s3_client.put_object(Body=image_data, Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=image_key)
#         image_url = 'https://{}.s3.amazonaws.com/{}'.format(settings.AWS_STORAGE_BUCKET_NAME, image_key)
        
#         return image_url
    
#     except Exception as e:
#         print("Exception occurred while uploading image to S3:", e)
#         return None
    
"""--------------아래 drf를 이용하는 코드로 바꿀 예정---------------------"""
from rest_framework import mixins,status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from botocore.exceptions import ClientError
from django.http import JsonResponse


from .serializers import *
from .models import *
from ai.generate_image import *
from fairy_tairy.permissions import *

import requests
import logging
import base64
import boto3
import uuid
import time
import io
import os

def request_image_from_flask(prompt):
    # Flask 서버의 URL
    # flask_url = 'http://localhost:5000/get_image'
    flask_url = 'http://34.64.98.73:5000/get_image'
    
    try:
        # HTTP POST 요청으로 prompt를 Flask에 전송
        response = requests.post(flask_url, json={'prompt': prompt},verify=False, timeout=150)
        # 응답 확인
        if response.status_code == 200:
            # 이미지 생성 성공
            response_data = response.json()
            image_url = response_data['image_url']
            print("Received image url:", image_url)
            time.sleep(2)
            return image_url
        else:
            # 이미지 생성 실패
            print("Failed to get image from Flask:", response.status_code)
            return None
    except Exception as e:
        print("Error:", e)
        time.sleep(10)
        return None

class ImageViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin):

    permission_classes = [IsAuthenticated]
    serializer_class = ImageAdminSerializer
    queryset = Image.objects.all()

    def filter_queryset(self,queryset):
        queryset = queryset.filter(diary__user=self.request.user)
        return super().filter_queryset(queryset)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            diary = serializer.validated_data.get('diary')
            image_prompt = get_prompt(diary.content)[0]
            print(image_prompt)
            
            image_url = request_image_from_flask(image_prompt)
            print('img: ',image_url)
            if not image_url:
                return Response({'error': "Failed to get image from Flask"}, status=status.HTTP_400_BAD_REQUEST)
                
            print('save')
            new_image = Image.objects.get_or_create(diary=diary, image_url=f"{image_url}.png", image_prompt=image_prompt)
            return Response({"message": "Image uploaded successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f"Error uploading image: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 이미지 삭제 기능
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 이미지 업데이트 기능
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    
class ImageAdminViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin):

    permission_classes = [IsAdminUser]
    serializer_class = ImageAdminSerializer
    queryset = Image.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            diary = serializer.validated_data.get('diary')
            image_prompt = get_prompt(diary.content)[0]
            print(image_prompt)
            
            image_url = request_image_from_flask(image_prompt)
            print('img: ',image_url)
            if not image_url:
                return Response({'error': "Failed to get image from Flask"}, status=status.HTTP_400_BAD_REQUEST)
                
            print('save')
            new_image = Image.objects.get_or_create(diary=diary, image_url=f"{image_url}.png", image_prompt=image_prompt)
            return Response({"message": "Image uploaded successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f"Error uploading image: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # 이미지 목록 조회 기능
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 이미지 삭제 기능
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 이미지 업데이트 기능
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)