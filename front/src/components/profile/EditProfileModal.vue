<template>
  <div v-if="show" class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">내 정보 수정</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <form @submit.prevent="handleSubmit" class="edit-form">
        <!-- 프로필 이미지 -->
        <div class="form-group">
          <div class="profile-image-container">
            <div class="profile-preview">
              <img 
                :src="getImageUrl(previewImage || initialData?.profile_image)"  
                alt="Profile" 
                class="profile-img"
              />
              <label for="profile-upload" class="image-upload-label">
                <span>이미지 변경</span>
                <input 
                  id="profile-upload"
                  type="file" 
                  @change="handleImageChange" 
                  accept="image/*"
                  class="file-input"
                >
              </label>
            </div>
          </div>
        </div>
        
        <!-- 닉네임 -->
        <div class="form-group">
          <label class="form-label">닉네임</label>
          <input 
            v-model="formData.nickname" 
            type="text" 
            class="form-input"
            :class="{ 'error': errors.nickname }"
            required
            placeholder="닉네임을 입력하세요"
          >
          <span v-if="errors.nickname" class="error-message">{{ errors.nickname }}</span>
        </div>

        <!-- 전화번호 -->
        <div class="form-group">
          <label class="form-label">전화번호</label>
          <input 
            v-model="formData.phone_num" 
            type="text" 
            class="form-input"
            :class="{ 'error': errors.phone_num }"
            placeholder="010-0000-0000"
          >
          <span v-if="errors.phone_num" class="error-message">{{ errors.phone_num }}</span>
        </div>

        <!-- 생년월일 -->
        <div class="form-group">
          <label class="form-label">생년월일</label>
          <input 
            v-model="formData.birth_date" 
            type="date" 
            class="form-input"
            :class="{ 'error': errors.birth_date }"
          >
          <span v-if="errors.birth_date" class="error-message">{{ errors.birth_date }}</span>
        </div>

        <div class="button-group">
          <button type="submit" class="submit-btn" :disabled="isSubmitting">
            {{ isSubmitting ? '수정 중...' : '수정하기' }}
          </button>
          <button type="button" class="cancel-btn" @click="$emit('close')">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores/user'

const baseURL = 'http://localhost:8000'

const getImageUrl = (imagePath) => {
  // null이거나 undefined인 경우 기본 이미지 경로 반환
  if (!imagePath) {
    return baseURL + '/static/images/default_profile.jpg'
  }
  
  // 미리보기 이미지
  if (imagePath.startsWith('data:')) {
    return imagePath
  }

  // 업로드된 이미지인 경우
  return baseURL + imagePath
}

const props = defineProps({
  show: Boolean,
  initialData: Object
})

const emit = defineEmits(['close', 'update'])
const userStore = useUserStore()

const formData = ref({
  nickname: props.initialData?.nickname || '',
  phone_num: props.initialData?.phone_num || '',
  birth_date: props.initialData?.birth_date || '',
  profile_image: null
})

const previewImage = ref(null)
const errors = ref({})
const isSubmitting = ref(false)

// 전화번호 유효성 검사
const validatePhoneNumber = (phone) => {
  if (!phone) return true  // 빈값은 허용
  const phoneRegex = /^010-\d{4}-\d{4}$/
  return phoneRegex.test(phone)
}

// 전화번호 입력시 자동 하이픈 추가 및 유효성 검사
watch(() => formData.value.phone_num, (newVal) => {
  if (!newVal) {
    errors.value.phone_num = ''
    return
  }

  // 숫자만 추출
  const numbers = newVal.replace(/[^\d]/g, '')
  
  // 형식에 맞게 하이픈 추가
  if (numbers.length >= 11) {
    formData.value.phone_num = `${numbers.slice(0,3)}-${numbers.slice(3,7)}-${numbers.slice(7,11)}`
  }
  
  // 유효성 검사
  if (!validatePhoneNumber(formData.value.phone_num)) {
    errors.value.phone_num = '올바른 전화번호 형식이 아닙니다. (예: 010-0000-0000)'
  } else {
    errors.value.phone_num = ''
  }
})

const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.value.profile_image = file
    // 이미지 미리보기
    const reader = new FileReader()
    reader.onload = (e) => {
      previewImage.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const validateForm = () => {
  errors.value = {}
  let isValid = true

  if (!formData.value.nickname) {
    errors.value.nickname = '닉네임을 입력해주세요.'
    isValid = false
  }

  if (formData.value.phone_num && !validatePhoneNumber(formData.value.phone_num)) {
    errors.value.phone_num = '올바른 전화번호 형식이 아닙니다.'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isSubmitting.value = true
  try {
    await userStore.update(formData.value)
    emit('update')
    emit('close')
  } catch (err) {
    console.error('업데이트 실패:', err)
    if (err.response?.data) {
      errors.value = err.response.data
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: #1a0b2e;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.modal-title {
  font-size: 1.5rem;
  color: white;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #c8c8c8;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: white;
}

.profile-image-container {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.profile-preview {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
}

.profile-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-upload-label {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  text-align: center;
  padding: 8px 0;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.image-upload-label:hover {
  background: rgba(0, 0, 0, 0.8);
}

.file-input {
  display: none;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #333;
  border-radius: 6px;
  background: #2d1b4e;
  color: white;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: #666;
}

.form-input:focus {
  border-color: #8346ff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(131, 70, 255, 0.2);
}

.form-input.error {
  border-color: #ff4444;
}

.error-message {
  color: #ff4444;
  font-size: 0.8rem;
  margin-top: 0.25rem;
  display: block;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.submit-btn, .cancel-btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
}

.submit-btn {
  background: #8346ff;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #9666ff;
}

.submit-btn:disabled {
  background: #666;
  cursor: not-allowed;
}

.cancel-btn {
  background: #333;
  color: white;
}

.cancel-btn:hover {
  background: #444;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 스크롤바 스타일링 */
.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: #1a0b2e;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: #8346ff;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .modal-content {
    padding: 1.5rem;
  }

  .form-input {
    padding: 0.6rem;
  }

  .button-group {
    flex-direction: column;
  }

  .submit-btn, .cancel-btn {
    width: 100%;
  }
}
</style>