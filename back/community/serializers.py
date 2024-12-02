# community/serializers.py
from django.db import models
from rest_framework import serializers
from .models import Discussion, Report
from django.contrib.auth import get_user_model

class DiscussionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'profile_image')

class DiscussionSerializer(serializers.ModelSerializer):
    user = DiscussionUserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    is_reported = serializers.SerializerMethodField()
    report_reason = serializers.SerializerMethodField()  # 추가
    
    class Meta:
        model = Discussion
        fields = ('id', 'user', 'username', 'movie', 'movie_title', 'content', 
            'created_at', 'is_hidden', 'report_count', 'is_reported', 'report_reason')
        read_only_fields = ('created_at',)

    def get_is_reported(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.reports.filter(reporter=request.user).exists()
        return False

    def get_report_reason(self, obj):
        # 가장 많이 신고된 이유를 반환
        most_common_reason = obj.reports.values('reason')\
            .annotate(count=models.Count('reason'))\
            .order_by('-count')\
            .first()
        return most_common_reason['reason'] if most_common_reason else None

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'discussion', 'reason', 'content', 'created_at')
        read_only_fields = ('reporter',)
