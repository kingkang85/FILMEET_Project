from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.get_movie_recommendation, name='movie-recommendation'),
    path('recommend/fallback/', views.fallback_recommendation, name='fallback-recommendation'),
]