from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserSerializer, UserUpdateSerializer
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
import random
import string

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_account(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    
    try:
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '회원정보가 성공적으로 수정되었습니다.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': '입력하신 정보가 올바르지 않습니다.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'error': '회원정보 수정 중 오류가 발생했습니다.',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    request.user.delete()
    return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=204)

@api_view(['GET'])
def find_username(request):
    try:
        email = request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        
        return Response({
            'message': '아이디를 찾았습니다.',
            'username': user.username
        })
    
    except User.DoesNotExist:
        return Response(
            {'error': '해당 이메일로 가입된 계정이 없습니다.'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
def reset_password(request):
    try:
        email = request.data.get('email')  # POST 데이터에서 이메일 가져오기
        user = get_object_or_404(User, email=email)  # 이메일로 사용자 검색

        # 임시 비밀번호 생성
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        # 사용자 비밀번호 설정
        user.set_password(temp_password)
        user.save()

        # 이메일 전송
        send_mail(
            '[FILMEET] 임시 비밀번호 발급',
            f'''
            안녕하세요. {user.nickname}님!
            
            임시 비밀번호가 발급되었습니다.
            임시 비밀번호: {temp_password}
            
            로그인 후 반드시 비밀번호를 변경해 주세요!
            ''',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        
        return Response({'message': '임시 비밀번호가 이메일로 발송되었습니다.'})
    
    except User.DoesNotExist:
        return Response(
            {'error': '해당 이메일로 가입된 계정이 없습니다.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        # 현재 비밀번호 확인
        if not user.check_password(current_password):
            return Response(
                {'error': '현재 비밀번호가 일치하지 않습니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 새 비밀번호 설정
        user.set_password(new_password)
        user.save()

        return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'})

    except Exception as e:
        return Response(
            {'error': '비밀번호 변경 중 오류가 발생했습니다.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

