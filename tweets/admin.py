from django.contrib import admin
from .models import Tweet, Like

class ElonMuskFilter(admin.SimpleListFilter):
    title = 'Elon Musk'
    parameter_name = 'elon_musk'

    def lookups(self, request, model_admin):
        return [('yes', 'Contains'), ('no', 'Does not contain')]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(payload__icontains='Elon Musk')
        if self.value() == 'no':
            return queryset.exclude(payload__icontains='Elon Musk')

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payload', 'like_count', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('payload', 'user__username')
    list_filter = ('created_at', ElonMuskFilter)

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tweet', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)