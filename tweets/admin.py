from django.contrib import admin
from .models import Tweet, Like


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payload', 'like_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'user')
    search_fields = ('payload', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tweet', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'tweet__payload')
    readonly_fields = ('created_at', 'updated_at')