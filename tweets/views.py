from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tweet
from .serializers import TweetSerializer


def tweet_list(request):
    """템플릿 렌더링용 view (기존 유지)"""
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request, "tweets/tweet_list.html", {"tweets": tweets})


class TweetListAPIView(APIView):
    """
    트윗 목록 조회 및 생성 APIView
    GET: 모든 트윗 목록 조회
    """

    def get(self, request):
        """모든 트윗 목록을 최신순으로 조회"""
        tweets = Tweet.objects.all().select_related("user").prefetch_related(
            "likes__user"
        ).order_by("-created_at")
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)


class UserTweetsAPIView(APIView):
    """
    특정 사용자의 트윗 목록 조회 APIView
    GET: 사용자의 모든 트윗 목록 조회
    """

    def get(self, request, user_id):
        """특정 사용자의 트윗 목록 조회"""
        tweets = Tweet.objects.filter(user_id=user_id).select_related(
            "user"
        ).prefetch_related("likes__user").order_by("-created_at")
        serializer = TweetSerializer(tweets, many=True)
        return Response(
            {
                "tweets": serializer.data,
                "count": tweets.count(),
            }
        )
