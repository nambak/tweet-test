from django.urls import path
from . import views

urlpatterns = [
    path('tweets', views.tweet_list_api),
    path('users/<int:user_id>/tweets', views.user_tweets_api),
]