# ai_recommendation/services.py
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from django.db.models import Count, Avg, Q, F
from django.contrib.auth import get_user_model
from django.conf import settings
from openai import OpenAI
import logging
import random
from collections import Counter
from movies.models import (
    Movie, Genre, Actor, Director, 
    MovieGenre, MovieActor, MovieDirector
)
from movies.serializers import MovieSerializer

User = get_user_model()
logger = logging.getLogger(__name__)

@dataclass
class UserPreferences:
    genres: Counter
    actors: Counter
    directors: Counter
    
@dataclass
class RecommendationResult:
    movie: Dict
    message: str
    note: Optional[str] = None
    recommendation_type: str = 'ai'  # 'ai', 'personalized', 'keyword'
    
class MovieRecommender:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.keywords = {
            '액션': ['action', '액션', '전투', '격투'],
            '로맨스': ['romance', '로맨스', '사랑', '멜로'],
            '코미디': ['comedy', '코미디', '웃음', '유머'],
            '공포': ['horror', '공포', '무서운', '스릴러'],
            'SF': ['sf', '공상', '과학', '미래'],
            '판타지': ['fantasy', '판타지', '마법', '환상'],
            '드라마': ['drama', '드라마', '감동', '가족'],
            '애니메이션': ['animation', '애니', '만화', '애니메이션']
        }

    def analyze_user_preferences(self, user_id: int) -> UserPreferences:
        """사용자의 위시리스트를 분석하여 선호도 정보를 추출"""
        user = User.objects.get(id=user_id)
        wishlist_movies = user.wishlist_movies.all()
        
        # 장르 선호도 분석
        genre_preferences = Counter()
        for movie in wishlist_movies:
            genres = MovieGenre.objects.filter(movie=movie).values_list('genre__name', flat=True)
            genre_preferences.update(genres)
            
        # 배우 선호도 분석
        actor_preferences = Counter()
        for movie in wishlist_movies:
            actors = MovieActor.objects.filter(movie=movie).values_list('actor__name', flat=True)
            actor_preferences.update(actors)
            
        # 감독 선호도 분석
        director_preferences = Counter()
        for movie in wishlist_movies:
            directors = MovieDirector.objects.filter(movie=movie).values_list('director__name', flat=True)
            director_preferences.update(directors)
            
        return UserPreferences(
            genres=genre_preferences,
            actors=actor_preferences,
            directors=director_preferences
        )

    async def get_ai_recommendation(self, user_input: str, user_preferences: UserPreferences) -> Optional[str]:
        """GPT를 활용한 영화 추천"""
        try:
            # 사용자 선호도 정보를 프롬프트에 포함
            preferences_prompt = f"""
            사용자가 선호하는 장르: {', '.join(user_preferences.genres.keys())}
            선호하는 배우: {', '.join(user_preferences.actors.keys()[:3])}
            선호하는 감독: {', '.join(user_preferences.directors.keys()[:3])}
            """
            
            completion = await self.client.chat.completions.create(
                model="gpt-4-mini",
                messages=[{
                    "role": "system",
                    "content": f"""너는 영화 추천 전문가야. 사용자의 입력과 선호도를 기반으로 우리 DB에 있는 영화 하나를 추천해줘.
                    {preferences_prompt}
                    영화 제목만 응답해."""
                }, {
                    "role": "user",
                    "content": f"다음 조건으로 영화 하나만 추천해줘: {user_input}"
                }],
                max_tokens=50
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"AI recommendation failed: {str(e)}")
            return None

    def get_personalized_recommendation(
        self, 
        user_preferences: UserPreferences,
        excluded_movies: Set[int] = None
    ) -> Optional[Movie]:
        """사용자 선호도 기반 추천"""
        try:
            # 기본 쿼리셋
            queryset = Movie.objects.all()
            if excluded_movies:
                queryset = queryset.exclude(id__in=excluded_movies)

            # 장르 기반 필터링
            if user_preferences.genres:
                top_genres = [genre for genre, _ in user_preferences.genres.most_common(3)]
                queryset = queryset.filter(genres__name__in=top_genres)

            # 배우/감독 기반 필터링
            if user_preferences.actors or user_preferences.directors:
                actor_filter = Q()
                director_filter = Q()
                
                if user_preferences.actors:
                    top_actors = [actor for actor, _ in user_preferences.actors.most_common(3)]
                    actor_filter = Q(movieactor__actor__name__in=top_actors)
                    
                if user_preferences.directors:
                    top_directors = [director for director, _ in user_preferences.directors.most_common(2)]
                    director_filter = Q(moviedirector__director__name__in=top_directors)
                
                queryset = queryset.filter(actor_filter | director_filter)

            # 평점과 인기도를 고려한 정렬
            queryset = queryset.annotate(
                score=F('vote_average') * 0.7 + F('popularity') * 0.3
            ).order_by('-score')[:20]

            return random.choice(list(queryset)) if queryset else None

        except Exception as e:
            logger.error(f"Personalized recommendation failed: {str(e)}")
            return None

    def get_keyword_based_recommendation(
        self, 
        user_input: str,
        excluded_movies: Set[int] = None
    ) -> Tuple[Optional[Movie], List[str]]:
        """키워드 기반 추천"""
        matched_genres = []
        for genre, genre_keywords in self.keywords.items():
            if any(keyword in user_input.lower() for keyword in genre_keywords):
                matched_genres.append(genre)

        queryset = Movie.objects.filter(genres__name__in=matched_genres).distinct() if matched_genres \
                  else Movie.objects.all()
                  
        if excluded_movies:
            queryset = queryset.exclude(id__in=excluded_movies)
        
        top_movies = queryset.order_by('-vote_average')[:20]
        return (random.choice(list(top_movies)) if top_movies else None, matched_genres)

    async def recommend(self, user_input: str, user_id: int) -> RecommendationResult:
        """통합 추천 로직"""
        try:
            excluded_movies = set(
                Movie.objects.filter(wishlist_users=user_id).values_list('id', flat=True)
            )
            user_preferences = self.analyze_user_preferences(user_id)

            # 1. AI 추천 시도
            if ai_title := await self.get_ai_recommendation(user_input, user_preferences):
                if movie := Movie.objects.filter(title__icontains=ai_title).first():
                    return RecommendationResult(
                        movie=MovieSerializer(movie).data,
                        message=f'"{movie.title}"를 AI가 추천드립니다!',
                        recommendation_type='ai'
                    )

            # 2. 개인화 추천 시도
            if movie := self.get_personalized_recommendation(user_preferences, excluded_movies):
                return RecommendationResult(
                    movie=MovieSerializer(movie).data,
                    message=f'사용자님의 취향을 분석하여 "{movie.title}"를 추천드립니다!',
                    recommendation_type='personalized'
                )

            # 3. 키워드 기반 폴백
            movie, matched_genres = self.get_keyword_based_recommendation(user_input, excluded_movies)
            if not movie:
                raise ValueError('조건에 맞는 영화를 찾을 수 없습니다.')

            return RecommendationResult(
                movie=MovieSerializer(movie).data,
                message=f'"{movie.title}"를 추천드립니다!',
                note='현재 AI 서비스가 많이 사용되어 키워드 기반으로 추천해드렸습니다.' \
                     if matched_genres else None,
                recommendation_type='keyword'
            )

        except Exception as e:
            logger.error(f"Movie recommendation failed: {str(e)}")
            raise