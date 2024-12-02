from django.urls import path
from . import views

urlpatterns = [
    # 전체 댓글 목록
    path('discussions/', views.discussion_list, name='discussion-list'),
    # 특정 영화의 댓글 목록 및 생성
    path('movies/<int:movie_id>/discussions/', views.movie_discussion_list, name='movie-discussion-list'),
    # 특정 사용자의 댓글 목록
    path('users/<int:user_id>/discussions/', views.user_discussion_list, name='user-discussion-list'),
    # 댓글 수정 및 삭제
    path('discussions/<int:discussion_id>/', views.discussion_detail, name='discussion-detail'),
    path('discussions/<int:discussion_id>/report/', views.report_discussion, name='report-discussion'),
]