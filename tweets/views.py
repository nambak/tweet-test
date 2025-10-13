from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import Tweet
from django.contrib.auth.models import User
from .serializers import TweetSerializer
from .serializers import UserSerializer


def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request, "tweets/tweet_list.html", {"tweets": tweets})


class TweetList(APIView):
    def get(self, request):
        tweets = Tweet.objects.all().select_related("user").prefetch_related(
            "likes__user"
        ).order_by("-created_at")
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TweetDetail(APIView):
    def get(self, request, pk):
        tweet = Tweet.objects.get(pk=pk)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)
    def put(self, request, pk):
        tweet = Tweet.objects.get(pk=pk)
        serializer = TweetSerializer(tweet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tweet = Tweet.objects.get(pk=pk)
        tweet.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserTweets(APIView):
    def get(self, request, pk):
        tweets = Tweet.objects.filter(user_id=pk).select_related(
            "user"
        ).prefetch_related("likes__user").order_by("-created_at")
        serializer = TweetSerializer(tweets, many=True)
        return Response(
            {
                "tweets": serializer.data,
                "count": tweets.count(),
            }
        )
