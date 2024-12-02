from rest_framework import serializers
from .models import (
    Movie, Genre, MovieGenre,
    Actor, MovieActor,
    Director, MovieDirector,
    Ott, MovieOtt
)

# 영화-배우 관계에서 배우의 출연작 정보를 보여주기 위한 시리얼라이저
class MovieActorSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(source='movie.movie_id')
    title = serializers.CharField(source='movie.title')
    poster_path = serializers.CharField(source='movie.poster_path')
    release_date = serializers.DateField(source='movie.release_date')
    
    class Meta:
        model = MovieActor
        # 위에서 정의한 필드들과 character_name(MovieActor 모델의 원래 필드) 포함
        fields = ('movie_id', 'title', 'poster_path', 'release_date', 'character_name')


# 배우 상세 페이지를 위한 시리얼라이저 (배우 정보 + 출연작 목록)
class ActorDetailSerializer(serializers.ModelSerializer):
    filmography = MovieActorSerializer(source='movieactor_set', many=True)
    
    class Meta:
        model = Actor
        fields = ('person_id', 'name', 'profile_path', 'birth_date', 
                 'birthplace', 'biography', 'filmography')
        

# 영화-감독 관계에서 감독의 연출작 정보를 보여주기 위한 시리얼라이저
class MovieDirectorSerializer(serializers.ModelSerializer):
   movie_id = serializers.IntegerField(source='movie.movie_id')
   title = serializers.CharField(source='movie.title')
   poster_path = serializers.CharField(source='movie.poster_path')
   release_date = serializers.DateField(source='movie.release_date')
   
   class Meta:
       model = MovieDirector
       fields = ('movie_id', 'title', 'poster_path', 'release_date')


# 감독 상세 페이지를 위한 시리얼라이저 (감독 정보 + 연출작 목록)
class DirectorDetailSerializer(serializers.ModelSerializer):
   filmography = MovieDirectorSerializer(source='moviedirector_set', many=True)
   
   class Meta:
       model = Director
       fields = ('person_id', 'name', 'profile_path', 'birth_date', 
                'birthplace', 'biography', 'filmography')


# 영화 상세 페이지에서 출연진 정보를 보여주기 위한 시리얼라이저
class CastSerializer(serializers.ModelSerializer):
    # MovieActor를 통해 연결된 Actor의 정보를 가져옴
    id = serializers.IntegerField(source='actor.person_id')
    name = serializers.CharField(source='actor.name')
    profile_path = serializers.CharField(source='actor.profile_path')
    
    class Meta:
        model = MovieActor
        # 배우 기본 정보와 캐릭터 이름 포함
        fields = ('id', 'name', 'profile_path', 'character_name',)


# 영화-OTT 관계에서 OTT 정보를 보여주기 위한 시리얼라이저
class MovieOttSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ott.name')
    logo_path = serializers.CharField(source='ott.logo_path')
    
    class Meta:
        model = MovieOtt
        fields = ('name', 'logo_path')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('person_id', 'name', 'profile_path', 'gender')

class DirectorSerializer(serializers.ModelSerializer):
   class Meta:
       model = Director
       fields = '__all__'
       

# 영화 정보를 위한 메인 시리얼라이저
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True, source='genre_set')
    director = DirectorSerializer(source='director_set', many=True, read_only=True)
    providers = MovieOttSerializer(source='movieott_set', many=True, read_only=True)
    cast = CastSerializer(source='movieactor_set', many=True, read_only=True)

    class Meta:
        model = Movie
        exclude = ('wishlist_users',)
    
    # 영화 생성 시 장르 정보도 함께 저장
    def create(self, validated_data):
        genre_ids = self.context.get('genre_ids', [])
        movie = Movie.objects.create(**validated_data)
        
        for genre_id in genre_ids:
            genre, _ = Genre.objects.get_or_create(genre_id=genre_id)
            MovieGenre.objects.create(movie=movie, genre=genre)
            
        return movie
    

# 유저가 찜한 영화 정보
class MovieWishSerializer(serializers.ModelSerializer):
    providers = MovieOttSerializer(source='movieott_set', many=True, read_only=True)  # OTT 추천을 위해 함께 넘겨줌
    
    class Meta:
        model = Movie
        fields = ('movie_id', 'title', 'poster_path', 'providers',)

# 유저가 찜한 배우 정보
class ActorWishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('person_id', 'name', 'profile_path',)

# 유저가 찜한 감독 정보
class DirectorWishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('person_id', 'name', 'profile_path',)