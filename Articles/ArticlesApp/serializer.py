from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class Comment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
