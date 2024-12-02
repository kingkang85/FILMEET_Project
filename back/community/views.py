# community/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Discussion, Report
from .serializers import DiscussionSerializer, ReportSerializer
from movies.models import Movie

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def discussion_list(request):
    """모든 댓글 조회"""
    discussions = Discussion.objects.select_related('user', 'movie').all()
    serializer = DiscussionSerializer(discussions, many=True)
    return Response(serializer.data)

from rest_framework.pagination import PageNumberPagination
class DiscussionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movie_discussion_list(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    
    if request.method == 'GET':
        paginator = DiscussionPagination()
        # 오름차순 정렬 (오래된 순)
        discussions = Discussion.objects.filter(movie=movie)\
            .select_related('user')\
            .order_by('created_at')
        paginated_discussions = paginator.paginate_queryset(discussions, request)
        serializer = DiscussionSerializer(
            paginated_discussions, 
            many=True, 
            context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        serializer = DiscussionSerializer(data={
            'content': request.data.get('content'),
            'movie': movie.id
        }, context={'request': request})  # context 추가
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            # 새로운 인스턴스의 시리얼라이저를 생성하여 반환
            return Response(
                DiscussionSerializer(
                    serializer.instance,
                    context={'request': request}
                ).data,
                status=status.HTTP_201_CREATED
            )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_discussion_list(request, user_id):
    """특정 사용자의 모든 댓글 조회"""
    discussions = Discussion.objects.filter(user_id=user_id).select_related('movie')
    serializer = DiscussionSerializer(discussions, many=True)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    
    if discussion.user != request.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = DiscussionSerializer(
            discussion,
            data=request.data,
            partial=True,
            context={'request': request}  # context 추가
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        discussion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_discussion_list(request, user_id):
    discussions = Discussion.objects.filter(user_id=user_id).select_related('movie')
    serializer = DiscussionSerializer(discussions, many=True, context={'request': request})  # context 추가
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_discussion(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    
    # 자신의 댓글은 신고할 수 없음
    if discussion.user == request.user:
        return Response({'detail': '자신의 댓글은 신고할 수 없습니다.'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # 이미 신고한 경우
    if Report.objects.filter(discussion=discussion, reporter=request.user).exists():
        return Response({'detail': '이미 신고한 댓글입니다.'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ReportSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(
            discussion=discussion,
            reporter=request.user
        )
        
        # 신고 횟수 증가 및 자동 숨김 처리
        discussion.report_count += 1
        
        # 스포일러 신고는 1회만으로도 숨김 처리
        if (discussion.report_count >= 3 or 
            (serializer.validated_data['reason'] == 'spoiler' and 
             discussion.reports.filter(reason='spoiler').count() >= 1)):
            discussion.is_hidden = True
            
        discussion.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)