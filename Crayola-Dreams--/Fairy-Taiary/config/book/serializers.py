from rest_framework import serializers
from .models import Book,Page

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_title', 'author', 'description','created_at']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'