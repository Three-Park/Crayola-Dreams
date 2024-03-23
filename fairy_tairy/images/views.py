from django.shortcuts import render, redirect
from django.http import HttpResponse
import boto3
import urllib.parse
from .forms import ImageForm
from botocore.exceptions import NoCredentialsError
import fairy_tairy.settings as settingss
from ai.generate_image import *

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

# def upload_to_s3(file, bucket_name, s3_folder_path):
#     s3 = boto3.client('s3', aws_access_key_id=settingss.AWS_ACCESS_KEY_ID,
#                       aws_secret_access_key=settingss.AWS_SECRET_ACCESS_KEY)

#     try:
#         file.seek(0)
        
#         # 업로드
#         s3.upload_fileobj(file, bucket_name, s3_folder_path + file.name)
        
#         # 파일 닫기
#         file.close()
#         print("Upload Successful") 
#         return True
#     except FileNotFoundError:
#         print("The file was not found")
#         return False
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False
    
"""--------------아래 drf를 이용하는 코드로 바꿀 예정---------------------"""
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from .serializers import *
from .models import *
from ai.generate_image import *
from fairy_tairy.permissions import *
import boto3
import uuid

    
class ImageViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin):

    permission_classes = [IsAuthenticated]
    serializer_class = ImageAdminSerializer
    queryset = Image.objects.all()


    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset.filter(user = self.request.user))
    
    
    def perform_create(self, serializer):
        diary_instance = serializer.validated_data['diary']
        image_prompt = get_prompt(diary_instance.content)
        try:
            image = get_image(image_prompt)
        except Exception as e:
            return Response({'error': f"Error generating image: {str(e)}"}, status=HTTP_400_BAD_REQUEST)

        s3_client = boto3.client('s3')
        image_filename = f"{uuid.uuid4()}.png"
        try:
            s3_client.upload_fileobj(image, settings.AWS_STORAGE_BUCKET_NAME, image_filename)
            image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{image_filename}"
            serializer.save(image_prompt=image_prompt, image_url=image_url)
            return super().perform_create(serializer)
        except Exception as e:
            return Response({'error': f"Error uploading image to S3: {str(e)}"}, status=HTTP_400_BAD_REQUEST)


class ImageAdminViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin):

    permission_classes = [IsAdminUser]
    serializer_class = ImageAdminSerializer
    queryset = Image.objects.all()
    
    def perform_create(self, serializer):
        diary_instance = serializer.validated_data['diary']
        image_prompt = get_prompt(diary_instance.content)
        image_instance = get_image(image_prompt)
        serializer.save(image_prompt=image_prompt, image = image_instance)
        return super().perform_create(serializer)
