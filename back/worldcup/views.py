# worldcup/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movies.models import Actor
from .models import WorldCupGame, WorldCupMatch
from movies.serializers import ActorSerializer

@api_view(['POST'])
def start_game(request):
    category = request.data.get('category', 9)
    
    # 프로필 이미지가 있는 배우만 선택
    actors_query = Actor.objects.filter(profile_path__isnull=False)
    
    # 성별에 따른 필터링
    if category in [1, 2]:  
        actors_query = actors_query.filter(gender=category)
    else:  # category가 9(전체)인 경우
        actors_query = actors_query.filter(gender__in=[1, 2])
    
    # 32명의 배우를 랜덤으로 선택
    selected_actors = list(actors_query.order_by('?')[:32])
    
    # 게임 인스턴스 생성
    game = WorldCupGame.objects.create(
        user=request.user if request.user.is_authenticated else None,
        category=category,
    )
    
    # 첫 라운드(32강) 매치 생성
    matches = []
    for i in range(0, 32, 2):
        match = WorldCupMatch.objects.create(
            game=game,
            actor1=selected_actors[i],
            actor2=selected_actors[i+1],
            round=5,  # 32강
        )
        matches.append({
            'match_id': match.id,
            'actor1': ActorSerializer(selected_actors[i]).data,
            'actor2': ActorSerializer(selected_actors[i+1]).data,
            'round': 5
        })
    
    return Response({
        'game_id': game.id,
        'matches': matches,
    })

@api_view(['POST'])
def submit_match(request):
    match_id = request.data.get('match_id')
    winner_id = request.data.get('winner_id')
    current_round = request.data.get('round')
    
    try:
        # 현재 매치 업데이트
        match = WorldCupMatch.objects.get(id=match_id)
        winner = Actor.objects.get(person_id=winner_id)
        match.winner = winner
        match.save()
        
        game = match.game
        current_round_matches = WorldCupMatch.objects.filter(
            game=game,
            round=current_round
        )
        
        # 현재 라운드의 모든 매치가 완료되었는지 확인
        if not current_round_matches.filter(winner__isnull=True).exists():
            if current_round > 1:  # 결승이 아닌 경우
                # 다음 라운드 매치 생성
                winners = [m.winner for m in current_round_matches]
                next_round = current_round - 1
                next_matches = []
                
                for i in range(0, len(winners), 2):
                    next_match = WorldCupMatch.objects.create(
                        game=game,
                        actor1=winners[i],
                        actor2=winners[i+1],
                        round=next_round,
                    )
                    next_matches.append({
                        'match_id': next_match.id,
                        'actor1': ActorSerializer(winners[i]).data,
                        'actor2': ActorSerializer(winners[i+1]).data,
                        'round': next_round
                    })
                
                return Response({
                    'next_round': True,
                    'matches': next_matches,
                })
            else:
                # 결승전 종료
                game.winner = winner
                game.save()
                return Response({
                    'game_completed': True,
                    'winner': ActorSerializer(winner).data
                })
        
        # 현재 라운드가 아직 진행 중인 경우
        return Response({
            'next_round': False
        })
        
    except (WorldCupMatch.DoesNotExist, Actor.DoesNotExist):
        return Response(
            {'error': '잘못된 매치 또는 배우 ID입니다.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )