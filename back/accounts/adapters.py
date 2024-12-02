from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        data = form.cleaned_data
        
        # nickname은 필수값이므로 get만 사용
        user.nickname = data.get('nickname')
        # 나머지는 선택값이므로 기본값 처리
        user.phone_num = data.get('phone_num', '')
        user.birth_date = data.get('birth_date')
        user.profile_image = data.get('profile_image')
        user.points = 500  # 항상 500으로 설정
        
        if commit:
            user.save()
        return user