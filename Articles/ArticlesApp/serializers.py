from rest_framework import serializers
from .models import Category, Article, Comment, BookMarks


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
