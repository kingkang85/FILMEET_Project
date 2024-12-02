from django.db import models
from django.conf import settings
from movies.models import Actor

class WorldCupGame(models.Model):
    # 로그인 안 한 사용자도 플레이 가능
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) 
    category = models.IntegerField(default=9)  # 기본값을 9(전체)로 설정
    winner = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True)


class WorldCupMatch(models.Model):
    game = models.ForeignKey(WorldCupGame, on_delete=models.CASCADE)
    actor1 = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='matches_as_actor1')
    actor2 = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='matches_as_actor2')
    winner = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='match_wins', null=True)
    round = models.IntegerField()  # 32강=5, 16강=4, 8강=3, 4강=2, 결승=1