import os
import django
import requests
from datetime import datetime

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_project.settings')
django.setup()

# Django 모델 임포트 (프로젝트 구조에 맞게 경로 수정 필요)
from movies.models import Movie, Genre, Director, Actor, Ott, MovieDirector, MovieActor, MovieOtt
from movies.serializers import MovieSerializer

def fetch_and_save_movie_data():
    # API 키 설정
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY environment variable is not set")

    # 장르 데이터 저장
    GENRE_URL = f'https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=ko-KR'
    genre_response = requests.get(GENRE_URL)
    if genre_response.status_code == 200:
        genres_data = genre_response.json()['genres']
        for genre in genres_data:
            Genre.objects.get_or_create(
                genre_id=genre['id'],
                defaults={'name': genre['name']}
            )
        print(f"Genres saved/updated")
    else:
        print(f"Failed to fetch genre data: {genre_response.status_code}")
        return

    # 영화 데이터 저장
    URL = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page='
    
    try:
        for num in range(1, 10):
            MOVIE_URL = URL + str(num)
            print(f"\nFetching page {num}...")
            
            movie_response = requests.get(MOVIE_URL)
            if movie_response.status_code != 200:
                print(f"Failed to fetch movie data for page {num}")
                continue

            movie_data = movie_response.json()['results']

            for movie in movie_data:
                try:
                    # 영화 상세 정보 가져오기
                    DETAIL_URL = f'https://api.themoviedb.org/3/movie/{movie["id"]}?api_key={TMDB_API_KEY}&language=ko-KR'
                    detail_response = requests.get(DETAIL_URL)
                    runtime = None
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        runtime = detail_data.get('runtime')

                    # 비디오 정보 가져오기
                    VIDEO_URL = f'https://api.themoviedb.org/3/movie/{movie["id"]}/videos?api_key={TMDB_API_KEY}&language=ko-KR'
                    video_response = requests.get(VIDEO_URL)
                    video = None
                    if video_response.status_code == 200:
                        video_data = video_response.json()['results']
                        if video_data:
                            video = 'https://youtube.com/embed/' + video_data[0]['key']

                    movie_info = {
                        'movie_id': movie['id'],
                        'title': movie['title'],
                        'original_title': movie['original_title'],
                        'overview': movie['overview'],
                        'release_date': movie['release_date'],
                        'poster_path': f"https://image.tmdb.org/t/p/w300/{movie['poster_path']}" if movie['poster_path'] else None,
                        'vote_average': movie['vote_average'],
                        'popularity': movie['popularity'],
                        'original_language': movie['original_language'],
                        'video_path': video,
                        'runtime': runtime
                    }

                    # 영화 정보 저장
                    if all(movie_info.values()):
                        if not Movie.objects.filter(movie_id=movie['id']).exists():
                            serializer = MovieSerializer(
                                data=movie_info,
                                context={'genre_ids': movie['genre_ids']}
                            )
                            if serializer.is_valid():
                                movie_instance = serializer.save()
                                print(f"Saved movie: {movie['title']}")

                                # 출연진과 감독 정보 저장
                                save_credits(movie_instance, movie['id'], TMDB_API_KEY)
                                
                                # OTT 정보 저장
                                save_ott_providers(movie_instance, movie['id'], TMDB_API_KEY)
                            else:
                                print(f"Validation error for movie {movie['title']}: {serializer.errors}")

                except Exception as e:
                    print(f"Error processing movie {movie.get('title', 'Unknown')}: {str(e)}")
                    continue

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# 출연진과 감독 정보를 저장하는 함수
def save_credits(movie_instance, movie_id, api_key):
    CREDIT_URL = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=ko-KR'
    credit_response = requests.get(CREDIT_URL)
    
    if credit_response.status_code == 200:
        credit_data = credit_response.json()
        
        # 감독 정보 저장
        director_data = next(
            (crew for crew in credit_data.get('crew', []) 
             if crew['job'] == 'Director'), None
        )
        if director_data:
            save_director(movie_instance, director_data, api_key)

        # 배우 정보 저장 (상위 5명)
        cast_data = sorted(credit_data.get('cast', []), 
                         key=lambda x: x.get('order', 999))[:5]
        for cast in cast_data:
            save_actor(movie_instance, cast, api_key)


# 감독 정보를 저장하는 함수
def save_director(movie_instance, director_data, api_key):
    PERSON_URL = f'https://api.themoviedb.org/3/person/{director_data["id"]}?api_key={api_key}&language=ko-KR'
    person_res = requests.get(PERSON_URL)
    
    if person_res.status_code == 200:
        person_data = person_res.json()
        director, _ = Director.objects.get_or_create(
            person_id=director_data['id'],
            defaults={
                'name': person_data['name'],
                'profile_path': f"https://image.tmdb.org/t/p/w300{person_data['profile_path']}" if person_data.get('profile_path') else None,
                'birth_date': person_data.get('birthday'),
                'birthplace': person_data.get('place_of_birth'),
                'biography': person_data.get('biography')
            }
        )
        MovieDirector.objects.get_or_create(
            movie=movie_instance,
            director=director
        )
        print(f"Added director: {person_data['name']}")


# 배우 정보를 저장하는 함수
def save_actor(movie_instance, cast_data, api_key):
    PERSON_URL = f'https://api.themoviedb.org/3/person/{cast_data["id"]}?api_key={api_key}&language=ko-KR'
    person_res = requests.get(PERSON_URL)
    
    if person_res.status_code == 200:
        person_data = person_res.json()
        actor, _ = Actor.objects.get_or_create(
            person_id=cast_data['id'],
            defaults={
                'name': person_data['name'],
                'profile_path': f"https://image.tmdb.org/t/p/w300{person_data['profile_path']}" if person_data.get('profile_path') else None,
                'birth_date': person_data.get('birthday'),
                'birthplace': person_data.get('place_of_birth'),
                'biography': person_data.get('biography'),
                'gender': person_data.get('gender')
            }
        )
        MovieActor.objects.get_or_create(
            movie=movie_instance,
            actor=actor,
            defaults={'character_name': cast_data.get('character')}
        )
        print(f"Added actor: {person_data['name']}")


# OTT 제공자 정보를 저장하는 함수
def save_ott_providers(movie_instance, movie_id, api_key):
    PROVIDERS_URL = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}'
    providers_response = requests.get(PROVIDERS_URL)
    
    if providers_response.status_code == 200:
        providers_data = providers_response.json()
        kr_data = providers_data.get('results', {}).get('KR', {})
        
        for provider in kr_data.get('flatrate', []):
            ott, _ = Ott.objects.get_or_create(
                provider_id=provider['provider_id'],
                defaults={
                    'name': provider['provider_name'],
                    'logo_path': f"https://image.tmdb.org/t/p/original{provider['logo_path']}"
                }
            )
            MovieOtt.objects.create(
                movie=movie_instance,
                ott=ott
            )
            print(f"Added OTT: {provider['provider_name']}")

if __name__ == '__main__':
    print("Starting movie data import...")
    start_time = datetime.now()
    
    try:
        fetch_and_save_movie_data()
    except Exception as e:
        print(f"Script failed: {str(e)}")
    finally:
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"\nImport process completed in {duration}")