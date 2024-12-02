from django.db import models

# 영화 정보
class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, null=True)
    overview = models.TextField(null=True)
    poster_path = models.CharField(max_length=255, null=True)
    release_date = models.DateField(null=True)
    runtime = models.IntegerField(null=True)
    original_language = models.CharField(max_length=10, null=True)
    vote_average = models.FloatField()
    popularity = models.FloatField()
    video_path = models.CharField(max_length=255, null=True)
    wishlist_users = models.ManyToManyField('accounts.User', related_name='wishlist_movies')

# OTT 정보
class Ott(models.Model):
    provider_id = models.IntegerField()
    name = models.CharField(max_length=50)
    logo_path = models.CharField(max_length=200, null=True)
    movies = models.ManyToManyField(Movie, through='MovieOTT')  # Movie 모델과 다대다 관계

# Movie - OTT 중계 테이블
class MovieOtt(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    ott = models.ForeignKey(Ott, on_delete=models.CASCADE)

# 장르 정보
class Genre(models.Model):
    genre_id = models.IntegerField()
    name = models.CharField(max_length=50, null=True)
    movies = models.ManyToManyField(Movie, through='MovieGenre')  # Movie 모델과 다대다 관계

# Movie - Genre 중계 테이블
class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

# 배우 정보
class Actor(models.Model):
    person_id = models.IntegerField()
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    birthplace = models.CharField(max_length=100, null=True)
    biography = models.TextField(null=True)
    gender = models.IntegerField(null=True)
    movies = models.ManyToManyField(Movie, through='MovieActor')  # Movie 모델과 다대다 관계
    wishlist_users = models.ManyToManyField('accounts.User', related_name='wishlist_actors')

# Movie - Actor 중계 테이블
class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100, null=True)  # 배역 이름 

# 감독 정보
class Director(models.Model):
    person_id = models.IntegerField()
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    birthplace = models.CharField(max_length=100, null=True)
    biography = models.TextField(null=True)
    movies = models.ManyToManyField(Movie, through='MovieDirector')
    wishlist_users = models.ManyToManyField('accounts.User', related_name='wishlist_directors')
   
# Movie - Director 중계 테이블
class MovieDirector(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)