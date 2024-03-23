from rest_framework import serializers
import fairy_tairy.settings as settings
from .models import *
from ai.generate_image import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['diary','created_at','image_url','image']
        
    def create(self,validated_data):
        image_instance = super().create(validated_data)
        image_instance.image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/images/{image_instance.image.name}"
        image_instance.save()
        return image_instance
        
        

class ImageAdminSerializer():
    class Meta:
        model = Image
        fields = '__all__'
        
    def create(self,validated_data):
        image_instance = super().create(validated_data)
        image_instance.image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/images/{image_instance.image.name}"
        image_instance.save()
        return image_instance
        


