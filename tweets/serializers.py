from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tweet, Like


class UserSerializer(serializers.ModelSerializer):
    """User 모델을 위한 ModelSerializer"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class LikeSerializer(serializers.ModelSerializer):
    """Like 모델을 위한 ModelSerializer"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TweetSerializer(serializers.ModelSerializer):
    """Tweet 모델을 위한 ModelSerializer (중첩된 관계 포함)"""
    user = UserSerializer(read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['id', 'payload', 'user', 'likes', 'likes_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        """트윗의 좋아요 개수를 반환"""
        return obj.likes.count()
