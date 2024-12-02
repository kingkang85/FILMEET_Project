from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_game),  # 게임 시작 요청
    path('submit_match/', views.submit_match),  # 각 라운드 결과 제출
]