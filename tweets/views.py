from django.shortcuts import render
from .models import Tweet


def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request, "tweets/tweet_list.html", {"tweets": tweets})
