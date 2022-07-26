from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('likes',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class Comment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)


class FavouiteCatgorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouiteCatgory
        fields = '__all__'

