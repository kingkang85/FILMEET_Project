<template>
  <div class="auth-container">
    <NavBar />
    
    <div class="auth-form">
      <h1 class="auth-title">회원가입</h1>
      <p class="auth-subtitle">FILMEET 의 회원이 되어 다양한 혜택을 누려보세요!</p>
      
      <form @submit.prevent="handleSubmit">
        <!-- 기존 필드들 -->
        <div class="form-group">
          <label class="auth-label">아이디</label>
          <input 
            v-model="formData.username"
            type="text" 
            placeholder="아이디를 입력해 주세요." 
            id="id"
            class="auth-input"
            required 
          />
          <span v-if="errors.username" class="error-message">{{ errors.username[0] }}</span>
        </div>
        
        <div class="form-group">
          <label class="auth-label">비밀번호</label>
          <input 
            v-model="formData.password1"
            type="password" 
            placeholder="비밀번호는 8글자 이상 입력해 주세요." 
            class="auth-input"
            required 
          />
          <span v-if="errors.password1" class="error-message">{{ errors.password1[0] }}</span>
        </div>
        
        <div class="form-group">
          <label class="auth-label">비밀번호 확인</label>
          <input 
            v-model="formData.password2"
            type="password" 
            placeholder="비밀번호 확인" 
            class="auth-input"
            required 
          />
          <span v-if="errors.password2" class="error-message">{{ errors.password2[0] }}</span>
        </div>
        
        <div class="form-group">
          <label class="auth-label">닉네임</label>
          <input 
            v-model="formData.nickname"
            type="text" 
            placeholder="닉네임을 입력해 주세요." 
            class="auth-input"
            required 
          />
          <span v-if="errors.nickname" class="error-message">{{ errors.nickname[0] }}</span>
        </div>
       
        <div class="form-group">
          <label class="auth-label">이메일</label>
          <input 
            v-model="formData.email"
            type="email"
            placeholder="유효한 이메일을 입력해 주세요." 
            class="auth-input"
            required 
          />
          <span v-if="errors.email" class="error-message">{{ errors.email[0] }}</span>
        </div>

        <div class="form-group">
          <label class="auth-label">전화번호 (선택)</label>
          <input 
            v-model="formData.phone_num"
            type="tel" 
            placeholder="010-0000-0000" 
            class="auth-input" 
          />
          <span v-if="errors.phone_num" class="error-message">{{ errors.phone_num[0] }}</span>
        </div>

        <div class="form-group">
          <label class="auth-label">생년월일 (선택)</label>
          <input 
            v-model="formData.birth_date"
            type="date"
            value="2024-11-21"
            min="1900-01-01"
            max="2024-11-28"
            placeholder="생년월일 (선택)"
            class="auth-input"
          />
          <span v-if="errors.birth_date" class="error-message">{{ errors.birth_date[0] }}</span>
        </div>

        <div class="form-group">
          <label class="auth-label">프로필 이미지 (선택)</label>
          <input 
            type="file" 
            @change="handleFileChange"
            accept="image/*"
            class="auth-input file-input" 
          />
          <span v-if="errors.profile_image" class="error-message">{{ errors.profile_image[0] }}</span>
          
          <!-- 이미지 미리보기 -->
          <div v-if="imagePreview" class="image-preview">
            <img :src="imagePreview" alt="프로필 이미지 미리보기" class="preview-image">
          </div>
        </div>
        
        <button 
          type="submit" 
          class="auth-button"
          :disabled="userStore.isLoading"
        >
          {{ userStore.isLoading ? '처리중...' : '회원가입' }}
        </button>
      </form>

      <div class="auth-message" v-if="errors.non_field_errors">
        {{ errors.non_field_errors[0] }}
      </div>
    </div>
  </div>
</template>

<script setup>
import NavBar from '@/components/common/NavBar.vue'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const errors = ref({})
const imagePreview = ref(null)

const formData = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
  nickname: '',
  phone_num: '',
  birth_date: '',
  profile_image: null
})

// 전화번호 유효성 검사 함수
const validatePhoneNumber = (phone) => {
  if (!phone) return true  // 빈값은 허용
  const phoneRegex = /^010-\d{4}-\d{4}$/
  return phoneRegex.test(phone)
}

// 전화번호 입력시 자동 하이픈 추가 및 유효성 검사
watch(() => formData.value.phone_num, (newVal) => {
  if (!newVal) {
    errors.value.phone_num = null
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
    errors.value.phone_num = ['올바른 전화번호 형식이 아닙니다. (예: 010-0000-0000)']
  } else {
    errors.value.phone_num = null
  }
})

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.value.profile_image = file
    // 이미지 미리보기 생성
    const reader = new FileReader()
    reader.onload = e => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const validateForm = () => {
  let isValid = true
  
  // 전화번호 유효성 검사
  if (formData.value.phone_num && !validatePhoneNumber(formData.value.phone_num)) {
    errors.value.phone_num = ['올바른 전화번호 형식이 아닙니다.']
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  try {
    errors.value = {}
    console.log('전송 데이터:', formData.value)
    await userStore.register(formData.value)
    alert('회원가입이 완료되었습니다!')
    router.push({ name: 'login' })
  } catch (error) {
    console.log('에러 응답:', error.response?.data)
    errors.value = error.response?.data || { 
      non_field_errors: ['회원가입 중 오류가 발생했습니다.'] 
    }
  }
}
</script>

<style scoped>
.auth-container {
  color: white;
}

.auth-form {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
}

.auth-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.auth-subtitle {
  text-align: center;
  font-size: 0.9rem;
  color: #c8c8c8;
  margin-bottom: 2rem;
  white-space: nowrap;
}

.form-group {
  margin-bottom: 1rem;
}

.auth-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #333;
  border-radius: 4px;
  background-color: transparent;
  color: white;
  outline: none;
}

.auth-input:focus {
  border-color: #8346ff;  /* 보라색 테두리 */
  box-shadow: 0 0 0 2px rgba(131, 70, 255, 0.2);  /* 보라색 그림자 효과 */
}

/* 달력 아이콘 색상 변경 */
.auth-input::-webkit-calendar-picker-indicator {
  filter: invert(1);
}
.auth-input::-moz-calendar-picker-indicator {
  filter: invert(1);
}
.auth-input::-ms-calendar-picker-indicator {
  filter: invert(1);
}

.auth-input::placeholder {
  color: #666;
}

.auth-button {
  width: 100%;
  padding: 0.8rem;
  background-color: #8346ff;
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

.auth-button:disabled {
  background-color: #555;
  cursor: not-allowed;
}

.auth-label {
  display: block;
  margin-bottom: 0.5rem;
  color: #c8c8c8;
  font-size: 0.9rem;
}

.file-input {
  padding: 0.5rem;
}

.file-input::-webkit-file-upload-button {
  background-color: #333;
  color: white;
  padding: 0.5rem 1rem;
  margin-right: 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.file-input::-webkit-file-upload-button:hover {
  background-color: #444;
}

.image-preview {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.preview-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;  /* 둥근 모서리 */
  object-fit: cover;   /* 이미지 비율 유지하면서 채우기 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  /* 그림자 효과 */
}

.error-message {
  color: #ff4b4b;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.auth-message {
  color: #ff4b4b;
  text-align: center;
  margin-top: 0.5rem;
}
</style>