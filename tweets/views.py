from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError

from .models import Tweet
from django.contrib.auth.models import User
from .serializers import TweetSerializer, PrivateUserSerializer
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
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required")
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

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

class ChangePassword(APIView):
    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=HTTP_200_OK)
        else:
            raise ParseError

class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "wrong password"})

class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})