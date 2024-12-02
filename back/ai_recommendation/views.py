# ai_recommendation/views.py
import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from movies.models import Movie
from movies.serializers import MovieSerializer
from openai import OpenAI, RateLimitError
from django.conf import settings
from django.db.models import Q

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class AIServiceError(Exception):
    """AI 서비스 관련 커스텀 예외"""
    pass

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_movie_recommendation(request):
    try:
        user_input = request.data.get('user_input', '')
        exclude_movie_ids = request.data.get('excludeWishlisted', [])
        
        if not user_input:
            return Response({
                'error': '입력값이 필요합니다.',
                'code': 'INVALID_INPUT'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logger.debug(f"Received user input: {user_input}")
        logger.debug(f"Excluding movie IDs: {exclude_movie_ids}")
        
        # 전체 영화 수 vs 제외할 영화 수 체크
        total_movies = Movie.objects.count()
        if exclude_movie_ids and len(exclude_movie_ids) >= total_movies:
            return Response({
                'error': '모든 영화가 찜 목록에 있습니다.',
                'code': 'ALL_MOVIES_WISHLISTED',
                'suggestion': '찜한 영화 제외 옵션을 해제하고 다시 시도해보세요.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # OpenAI API 호출
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "너는 영화 추천 전문가야. 사용자의 입력을 기반으로 우리 DB에 있는 영화 하나를 추천해줘. 영화 제목만 응답해."
                }, {
                    "role": "user",
                    "content": f"다음 조건으로 영화 하나만 추천해줘: {user_input}"
                }],
                max_tokens=50
            )
            
            recommended_title = completion.choices[0].message.content.strip()
            logger.debug(f"AI recommended title: {recommended_title}")
            
            # 영화 검색
            base_queryset = Movie.objects.all()
            if exclude_movie_ids:
                base_queryset = base_queryset.exclude(movie_id__in=exclude_movie_ids)
            
            movie = base_queryset.filter(title__icontains=recommended_title).first()
            
            if not movie:
                logger.debug(f"AI recommended movie not found: {recommended_title}")
                raise AIServiceError("AI가 추천한 영화를 찾을 수 없습니다.")
            
            serializer = MovieSerializer(movie)
            return Response({
                'movie': serializer.data,
                'message': f'"{movie.title}"를 추천드립니다!',
                'recommendation_type': 'ai'
            })
            
        except RateLimitError as e:
            logger.warning(f"OpenAI rate limit exceeded: {str(e)}")
            return Response({
                'error': 'AI 서비스 사용량이 초과되었습니다.',
                'code': 'RATE_LIMIT_EXCEEDED',
                'status': 429
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
        except AIServiceError as e:
            logger.info(f"Falling back to keyword recommendation: {str(e)}")
            return fallback_recommendation(request)
            
        except Exception as e:
            logger.error(f"AI recommendation failed: {str(e)}")
            return fallback_recommendation(request)
            
    except Exception as e:
        logger.error(f"Unexpected error in recommendation service: {str(e)}")
        return Response({
            'error': '영화 추천 서비스에 일시적인 문제가 발생했습니다.',
            'code': 'SYSTEM_ERROR'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fallback_recommendation(request):
    try:
        user_input = request.data.get('user_input', '').lower()
        exclude_movie_ids = request.data.get('excludeWishlisted', [])
        
        logger.info("Starting fallback recommendation")
        total_movies = Movie.objects.count()
        
        if exclude_movie_ids and len(exclude_movie_ids) >= total_movies:
            return Response({
                'error': '모든 영화가 찜 목록에 있습니다.',
                'code': 'ALL_MOVIES_WISHLISTED',
                'suggestion': '찜한 영화 제외 옵션을 해제하고 다시 시도해보세요.'
            }, status=status.HTTP_400_BAD_REQUEST)

        base_queryset = Movie.objects.all()
        if exclude_movie_ids:
            base_queryset = base_queryset.exclude(movie_id__in=exclude_movie_ids)

        # 장르 키워드 매칭
        keywords = {
            '액션': ['action', '액션', '전투', '격투'],
            '로맨스': ['romance', '로맨스', '사랑', '멜로'],
            '코미디': ['comedy', '코미디', '웃음', '유머'],
            '공포': ['horror', '공포', '무서운', '스릴러'],
            'SF': ['sf', '공상', '과학', '미래'],
            '판타지': ['fantasy', '판타지', '마법', '환상'],
            '드라마': ['drama', '드라마', '감동', '가족'],
            '애니메이션': ['animation', '애니', '만화', '애니메이션']
        }

        matched_genres = [
            genre for genre, keywords_list in keywords.items()
            if any(keyword in user_input for keyword in keywords_list)
        ]

        if matched_genres:
            movies = base_queryset.filter(
                moviegenre__genre__name__in=matched_genres
            ).distinct()
            logger.debug(f"Found movies with genres: {matched_genres}")
        else:
            movies = base_queryset
            logger.debug("No genres matched, using all available movies")

        # 평점 기반 랜덤 선택
        import random
        top_movies = list(movies.order_by('-vote_average')[:20])
        
        if not top_movies:
            return Response({
                'error': '추천할 수 있는 영화가 없습니다.',
                'code': 'NO_MOVIES_AVAILABLE',
                'suggestion': '찜한 영화 제외 옵션을 해제하고 다시 시도해보세요.'
            }, status=status.HTTP_404_NOT_FOUND)

        movie = random.choice(top_movies)
        logger.info(f"Selected movie for recommendation: {movie.title}")
        
        serializer = MovieSerializer(movie)
        return Response({
            'movie': serializer.data,
            'message': f'"{movie.title}"를 추천드립니다!',
            'recommendation_type': 'keyword',
            'note': '키워드 기반으로 추천해드렸습니다.'
        })

    except Exception as e:
        logger.error(f"Fallback recommendation failed: {str(e)}")
        return Response({
            'error': '영화 추천 서비스에 일시적인 문제가 발생했습니다.',
            'code': 'FALLBACK_ERROR'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)