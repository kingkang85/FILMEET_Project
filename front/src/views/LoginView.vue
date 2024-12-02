<template>
  <div class="auth-container">
    <NavBar />

    <div v-if="showFindUsername" class="modal-overlay" @click="closeUsernameModal">
      <div class="modal-content" @click.stop>
        <!-- 아이디 찾기 입력 폼 -->
        <div v-if="!foundUsername">
          <h2 class="modal-title">아이디 찾기</h2>
          <p class="modal-subtitle">가입하신 이메일을 입력하시면 아이디를 알려드립니다.</p>
          
          <form @submit.prevent="handleFindUsername">
            <div class="form-group">
              <input
                v-model="findEmail"
                type="email"
                placeholder="이메일"
                class="auth-input"
                required
              />
              <span v-if="findUsernameError" class="error-message">{{ findUsernameError }}</span>
            </div>
            
            <button type="submit" class="auth-button" :disabled="isLoading">
              {{ isLoading ? '처리중...' : '아이디 찾기' }}
            </button>
          </form>
        </div>

        <!-- 아이디 찾기 결과 -->
        <div v-else class="result-container">
          <h2 class="modal-title">아이디 찾기 결과</h2>
          <p class="result-message">
            찾으시는 아이디는 <span class="highlight">{{ foundUsername }}</span> 입니다.
          </p>
          <button @click="closeUsernameModal" class="auth-button">
            확인
          </button>
        </div>
        
        <button class="modal-close" @click="closeUsernameModal">×</button>
      </div>
    </div>

    <!-- 비밀번호 찾기 모달 -->
    <div v-if="showPasswordReset" class="modal-overlay" @click="closePasswordModal">
      <div class="modal-content" @click.stop>
        <h2 class="modal-title">비밀번호 찾기</h2>
        <p class="modal-subtitle">가입하신 이메일로 임시 비밀번호를 발송해드립니다.</p>
        
        <form @submit.prevent="handlePasswordReset">
          <div class="form-group">
            <input
              v-model="resetEmail"
              type="email"
              placeholder="이메일"
              class="auth-input"
              required
            />
            <span v-if="resetError" class="error-message">{{ resetError }}</span>
          </div>
          
          <button type="submit" class="auth-button" :disabled="isLoading">
            {{ isLoading ? '처리중...' : '임시 비밀번호 발송' }}
          </button>
        </form>
        
        <button class="modal-close" @click="closePasswordModal">×</button>
      </div>
    </div>

    <div class="auth-form">
      <h1 class="auth-title">로그인</h1>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <input
            v-model="formData.username"
            type="text"
            placeholder="아이디"
            class="auth-input"
            required
          />
        </div>
        
        <div class="form-group">
          <input
            v-model="formData.password"
            type="password"
            placeholder="비밀번호"
            class="auth-input"
            required
          />
        </div>
        
        <button type="submit" class="auth-button">로그인</button>
        <div v-if="errors.non_field_errors" class="error-message login-error">
          {{ errors.non_field_errors[0] }}
        </div>
      </form>
      
      <div class="auth-links">
        <a @click="showFindUsername = true" class="small-link">아이디 찾기</a>
        <span class="divider"> | </span>
        <a @click="showPasswordReset = true" class="small-link">비밀번호 찾기</a>
      </div>
      <RouterLink :to="{name : 'signup'}" class="signup-link">
        <p class="auth-message">
          FILMEET 의 회원이 아니신가요? 지금 가입해 보세요.
        </p>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import NavBar from '@/components/common/NavBar.vue';
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()
const errors = ref({})

// 로그인 폼 데이터
const formData = ref({
  username: '',
  password: ''
})

// 아이디 찾기 관련 상태
const showFindUsername = ref(false)
const findEmail = ref('')
const findUsernameError = ref('')
const foundUsername = ref('')  // 찾은 아이디 저장

// 비밀번호 초기화 관련 상태
const showPasswordReset = ref(false)
const resetEmail = ref('')
const resetError = ref('')
const isLoading = ref(false)

const handleSubmit = async () => {
  try {
    errors.value = {}
    await userStore.login({
      username: formData.value.username,
      password: formData.value.password
    })
    // 로그인 성공 시 메인 페이지로 이동
    router.push('/main')
  } catch (error) {
    if (error.response?.status === 400) {
      errors.value = {
        non_field_errors: ['아이디 또는 비밀번호가 올바르지 않습니다.']
      }
    } else {
      errors.value = error.response?.data || { 
        non_field_errors: ['로그인 중 오류가 발생했습니다.'] 
      }
    }
  }
}

// 아이디 찾기 모달 닫기
const closeUsernameModal = () => {
  showFindUsername.value = false
  findEmail.value = ''
  findUsernameError.value = ''
  foundUsername.value = ''
}

// 비밀번호 찾기 모달 닫기
const closePasswordModal = () => {
  showPasswordReset.value = false
  resetEmail.value = ''
  resetError.value = ''
}

// 아이디 찾기 처리
const handleFindUsername = async () => {
  try {
    isLoading.value = true
    findUsernameError.value = ''
    
    const response = await axios.get('http://127.0.0.1:8000/api/v1/users/username/find/', {
      params: { email: findEmail.value }
    })
    
    foundUsername.value = response.data.username
  } catch (err) {
    console.log(err)
    if (err.response?.status === 404) {
      findUsernameError.value = '해당 이메일로 가입된 계정이 없습니다.'
    } else {
      findUsernameError.value = '오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'
    }
  } finally {
    isLoading.value = false
  }
}

const handlePasswordReset = async () => {
  try {
    isLoading.value = true
    resetError.value = ''
    
    await axios.post('http://127.0.0.1:8000/api/v1/users/password/reset/', {
      email: resetEmail.value
    })
    
    alert('임시 비밀번호가 이메일로 발송되었습니다.')
    closePasswordModal()
  } catch (err) {
    console.log(err)
    if (err.response?.status === 404) {
      resetError.value = '해당 이메일로 가입된 계정이 없습니다.'
    } else {
      resetError.value = '오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  background-color: #0b001a;
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
  color: #c8c8c8;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

/* 입력 필드 스타일 */
.auth-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #333;
  border-radius: 4px;
  background: #2d1b4e;
  color: white;
  outline: none;
  transition: all 0.3s ease;
}

.auth-input:focus {
  border-color: #8346ff;
  box-shadow: 0 0 0 2px rgba(131, 70, 255, 0.2);
}

.auth-input::placeholder {
  color: #9e9e9e;
}

/* 버튼 스타일 */
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
  background-color: #666;
  cursor: not-allowed;
}

/* 링크 스타일 */
.auth-links {
  text-align: center;
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  align-items: center;
}

.small-link {
  color: #c8c8c8;
  text-decoration: none;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.small-link:hover {
  color: #8346ff;
}

.divider {
  color: #666;
  margin: 0 0.5rem;
}

/* 회원가입 링크 스타일 */
.signup-link {
  text-decoration: none;
}

.auth-message {
  text-align: center;
  color: #c8c8c8;
  margin-top: 2rem;
  font-size: 0.8rem;
  transition: color 0.3s ease;
  padding: 0.5rem;
  border-radius: 4px;
  white-space: nowrap;
}

.signup-link:hover .auth-message {
  color: #8346ff;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #0b001a;
  padding: 2rem;
  border-radius: 8px;
  position: relative;
  width: 90%;
  max-width: 400px;
  transition: all 0.3s ease;
}

.modal-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  text-align: center;
}

.modal-subtitle {
  color: #c8c8c8;
  text-align: center;
  margin-bottom: 1.5rem;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

/* 결과 컨테이너 스타일 */
.result-container {
  text-align: center;
  animation: fadeIn 0.3s ease;
}

.result-message {
  margin: 2rem 0;
  font-size: 1.1rem;
  color: #c8c8c8;
}

.highlight {
  color: #8346ff;
  font-weight: bold;
  font-size: 1.2rem;
}

/* 에러 메시지 스타일 */
.error-message {
  color: #ff4444;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  display: block;
}

.login-error {
  text-align: center;
  margin-top: 0.8rem;
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .modal-content {
    padding: 1.5rem;
  }
}
</style>