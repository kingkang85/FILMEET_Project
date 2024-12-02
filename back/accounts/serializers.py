from rest_framework import serializers
from movies.serializers import MovieWishSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
import re

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'profile_image')

class UserSerializer(serializers.ModelSerializer):
    wishlist_movies = MovieWishSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = '__all__'

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname', 'phone_num', 'birth_date', 'profile_image')

    def validate_nickname(self, value):
        # 현재 사용자 제외 중복 체크
        if User.objects.exclude(pk=self.instance.pk).filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value
    
    # 전화번호 형식 검증 (예: 010-1234-5678)
    def validate_phone_num(self, value):
        if value in (None, ''):
            return None
        
        if not re.match(r'^\d{3}-\d{4}-\d{4}$', value):
            raise serializers.ValidationError("올바른 전화번호 형식이 아닙니다. (예: 010-1234-5678)")
    
        if User.objects.exclude(pk=self.instance.pk).filter(phone_num=value).exists():
            raise serializers.ValidationError("이미 사용 중인 전화번호입니다.")
        
        return value

    def update(self, instance, validated_data):
        if 'profile_image' in validated_data:
            # 이전 프로필 이미지 삭제 (기본 이미지는 삭제 X)
            if instance.profile_image and instance.profile_image.name != 'images/default_profile.jpg':
                instance.profile_image.delete(save=False)
                
        return super().update(instance, validated_data)

class RegisterSerializer(DefaultRegisterSerializer):
    nickname = serializers.CharField(required=True, max_length=50)  # 필수값
    phone_num = serializers.CharField(required=False, allow_blank=True, max_length=20)
    birth_date = serializers.DateField(required=False, allow_null=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value
    
    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def validate_phone_num(self, value):
        if value in (None, ''):  # 비어 있는 값 처리
            return None
        
        # 전화번호 형식 검증
        if not re.match(r'^\d{3}-\d{4}-\d{4}$', value):
            raise serializers.ValidationError("올바른 전화번호 형식이 아닙니다. (예: 010-1234-5678)")
        
        # 전화번호 중복 체크
        if User.objects.filter(phone_num=value).exists():
            raise serializers.ValidationError("이미 사용 중인 전화번호입니다.")
        
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        phone_num = self.validated_data.get('phone_num', '')
        
        # 빈 문자열이면 None으로 변경
        if phone_num == '':
            phone_num = None

        data.update({
            'nickname': self.validated_data.get('nickname'),
            'phone_num': phone_num,
            'birth_date': self.validated_data.get('birth_date'),
            'profile_image': self.validated_data.get('profile_image'),
            'points': 500  # 기본값 500으로 설정
        })
        return data