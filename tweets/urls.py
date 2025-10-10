from django.urls import path
from . import views

urlpatterns = [
    # Tweet 관련 URL
    path('tweets/', views.TweetListAPIView.as_view(), name='tweet-list'),

    # 사용자별 Tweet URL
    path('users/<int:user_id>/tweets/', views.UserTweetsAPIView.as_view(), name='user-tweets'),
]