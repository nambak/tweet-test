from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer


def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request, "tweets/tweet_list.html", {"tweets": tweets})


@api_view(['GET'])
def tweet_list_api(request):
    tweets = Tweet.objects.all()
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_tweets_api(request, user_id):
    tweets = Tweet.objects.filter(user_id=user_id)
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)
