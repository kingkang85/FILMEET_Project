from django.urls import path
from . import views

urlpatterns = [
    path('<int:movie_id>/', views.movie_detail),  # 영화 정보 요청
    path('actors/<int:actor_id>/', views.actor_detail),  # 배우 정보 요청
    path('directors/<int:director_id>/', views.director_detail),  # 감독 정보 요청
    path('movies/', views.get_movie_list),  # 영화 리스트 요청
    path('<int:movie_id>/wishlist/', views.wish_movie),  # 영화 찜 추가/제거
    path('wishlist/', views.get_movie_wish),  # 영화 찜 목록 요청
    path('actors/<int:actor_id>/wishlist/', views.wish_actor),  # 배우 찜 추가/제거
    path('actors/wishlist/', views.get_actor_wish),  # 배우 찜 목록 요청
    path('directors/<int:director_id>/wishlist/', views.wish_director),  # 감독 찜 추가/제거
    path('directors/wishlist/', views.get_director_wish),  # 감독 찜 목록 요청
]