from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tweet, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = LikeSerializer(read_only=True, many=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['id', 'payload', 'user', 'likes', 'likes_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'password',
            'is_superuser',
            'id',
            'is_staff',
            'is_active',
            'first_name',
            'last_name',
            'username',
            'email',
        )