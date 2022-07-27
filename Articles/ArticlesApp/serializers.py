from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializerview(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',]


class ArticlePublisherSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='publisher.username')
    class Meta:
        model = Article
        fields = '__all__'

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

class BookmarkArticlesSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    class Meta:
        model = Bookmark
        fields = '__all__'


class Comment_serializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['content', 'article', 'created_at', 'user', 'username']


class FavouiteCatgorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouiteCatgory
        fields = '__all__'



class FavouiteCatgoriesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = FavouiteCatgory
        fields = '__all__'
CategorySerializer