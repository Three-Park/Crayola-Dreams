from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_title', 'author', 'created_at']