from django.urls import path
from . import views

urlpatterns = [
    path('tweets/', views.TweetList.as_view()),
    path('tweets/<int:pk>', views.TweetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/password', views.ChangePassword.as_view()),
    path('users/login', views.Login.as_view()),
    path('users/logout', views.Logout.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('users/<int:pk>/tweets/', views.UserTweets.as_view()),
]