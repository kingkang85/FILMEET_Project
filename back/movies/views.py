from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Movie, Genre, Actor, MovieActor, Director, MovieDirector, Ott, MovieOtt
from .serializers import (
    MovieSerializer, ActorDetailSerializer, DirectorDetailSerializer,
    MovieWishSerializer, ActorWishSerializer, DirectorWishSerializer
)
import requests


# 영화와 관련된 모든 정보(장르, 배우, 감독, OTT)를 DB에서 조회
@api_view(['GET'])
def movie_detail(request, movie_id):
    try:
        movie = get_object_or_404(Movie, movie_id=movie_id)
        data = MovieSerializer(movie).data

        if request.user.is_authenticated:
            is_wished = movie in request.user.wishlist_movies.all()
            data['is_wished'] = is_wished
        else:
            data['is_wished'] = False
        return Response(data)
    
    except Exception as e:
        print(f"Error in movie_detail: {str(e)}")
        return Response({'error': str(e)}, status=500)

# 배우 정보와 출연작 목록을 DB에서 조회
@api_view(['GET'])
def actor_detail(request, actor_id):
    try:
        actor = get_object_or_404(Actor, person_id=actor_id)
        data = ActorDetailSerializer(actor).data

        if request.user.is_authenticated:
            is_wished = actor in request.user.wishlist_actors.all()
            data['is_wished'] = is_wished
        else:
            data['is_wished'] = False
        return Response(data)
        
    except Exception as e:
        print(f"Error in actor_detail: {str(e)}")
        return Response({'error': str(e)}, status=500)

# 감독 정보와 연출작 목록을 DB에서 조회
@api_view(['GET'])
def director_detail(request, director_id):
    try:
        director = get_object_or_404(Director, person_id=director_id)
        data = DirectorDetailSerializer(director).data

        if request.user.is_authenticated:
            is_wished = director in request.user.wishlist_directors.all()
            data['is_wished'] = is_wished
        else:
            data['is_wished'] = False
        return Response(data)
        
    except Exception as e:
        print(f"Error in director_detail: {str(e)}")
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_movie_list(request):
    try:
        movie = get_list_or_404(Movie)
        serializer = MovieSerializer(movie, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        print(f"Error in director_detail: {str(e)}")
        return Response({'error': str(e)}, status=500)

# 영화 찜 추가/제거
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wish_movie(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    user = request.user

    if movie in user.wishlist_movies.all():
        user.wishlist_movies.remove(movie)
        return Response({'status': 'removed'})
    else:
        user.wishlist_movies.add(movie)
        return Response({'status': 'added'})

# 유저의 영화 찜 목록 제공
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movie_wish(request):
    wishlist = request.user.wishlist_movies.all()
    serializer = MovieWishSerializer(wishlist, many=True)
    return Response(serializer.data)

# 배우 찜 추가/제거
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def wish_actor(request, actor_id):
    actor = get_object_or_404(Actor, person_id=actor_id)
    user = request.user

    if actor in user.wishlist_actors.all():
        user.wishlist_actors.remove(actor)
        return Response({'status': 'removed'})
    else:
        user.wishlist_actors.add(actor)
        return Response({'status': 'added'})

# 유저의 배우 찜 목록 제공
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_actor_wish(request):
    wishlist = request.user.wishlist_actors.all()
    serializer = ActorWishSerializer(wishlist, many=True)
    return Response(serializer.data)

# 감독 찜 추가/제거
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def wish_director(request, director_id):
    director = get_object_or_404(Director, person_id=director_id)
    user = request.user

    if director in user.wishlist_directors.all():
        user.wishlist_directors.remove(director)
        return Response({'status': 'removed'})
    else:
        user.wishlist_directors.add(director)
        return Response({'status': 'added'})

# 배우의 감독 찜 목록 제공
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_director_wish(request):
    wishlist = request.user.wishlist_directors.all()
    serializer = DirectorWishSerializer(wishlist, many=True)
    return Response(serializer.data)