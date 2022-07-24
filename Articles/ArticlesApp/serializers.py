from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class BookMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMarks
        fields = '__all__'


class Comment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
