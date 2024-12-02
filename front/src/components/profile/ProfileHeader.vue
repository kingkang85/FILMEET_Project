<template>
  <div class="profile-section">
    <div class="profile-container">
      <div class="profile-image-section">
        <img :src="getImageUrl(user.profile_image)" alt="Profile" class="profile-image" />
        <h1 class="nickname">{{ user.nickname }}</h1>
      </div>
      <div class="profile-info">
        <p class="email">📧 {{ user.email }}</p>
        <p class="join-date" v-if="user.birth_date">🎂 {{ user.birth_date }}</p>
        <p class="points">💰 보유 포인트 : {{ user.points }}p</p>
        <div class="button-group">
          <button class="profile-btn" @click="$emit('openModal')">
            <i class="fas fa-user-edit"></i> 정보 수정
          </button>
          <button class="profile-btn" @click="$emit('openPasswordModal')">
            <i class="fas fa-key"></i> 비밀번호 변경
          </button>
        </div>
        <button class="profile-btn danger" @click="confirmResign">
          <i class="fas fa-user-times"></i> 회원 탈퇴
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const baseURL = 'http://localhost:8000'

const getImageUrl = (imagePath) => {
  // 기본 이미지
  if (!imagePath) {
    return baseURL + '/static/images/default_profile.jpg'
  }
  
  // 업로드된 이미지인 경우
  return baseURL + imagePath
}

defineProps({
  user: {
    type: Object,
    required: true
  }
})

defineEmits(['openModal', 'openPasswordModal'])

const confirmResign = () => {
  const isConfirmed = confirm(
    '정말로 탈퇴하시겠습니까?\n탈퇴 시 모든 정보가 삭제되며 복구할 수 없습니다.'
  )
  if (isConfirmed) {
    handleResign()
  }
}

const handleResign = async () => {
  try {
    await userStore.resign()
    alert('회원 탈퇴가 완료되었습니다.')
  } catch (err) {
    console.error('회원탈퇴 중 오류 발생:', err)
  }
}
</script>

<style>
.profile-section {
  padding: 2rem;
  margin: 2rem auto;
  max-width: 1200px;
}

.profile-container {
  display: flex;
  gap: 2.5rem;
  align-items: flex-start;  /* 상단 정렬로 변경 */
}

.profile-image-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 4px 15px rgba(131, 70, 255, 0.3);
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  padding-top: 1rem;  /* 상단 여백 추가 */
}

.nickname {
  font-size: 2rem;
  font-weight: bold;
  color: white;
  margin: 0;
}

.email, .join-date, .points {
  color: #c8c8c8;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.profile-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #2d1b4e;
  color: white;
}

.profile-btn:hover {
  background-color: #3d2b5e;
  transform: translateY(-2px);
}

.profile-btn.danger {
  background-color: transparent;
  color: #ff4444;
  margin-top: 1rem;
  font-size: 0.9rem;
  padding: 0;
}

.profile-btn.danger:hover {
  color: #ff6666;
  text-decoration: underline;
  transform: none;
}

@media (max-width: 768px) {
  .profile-container {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .profile-info {
    width: 100%;
    align-items: center;
  }

  .button-group {
    flex-direction: column;
    width: 100%;
  }
  
  .profile-btn {
    width: 100%;
    justify-content: center;
  }

  .profile-btn.danger {
    margin-top: 1.5rem;
  }

  .email, .join-date, .points {
    justify-content: center;
  }
}
</style>