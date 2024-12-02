<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">비밀번호 변경</h2>
        <button class="modal-close" @click="closeModal">×</button>
      </div>

      <form @submit.prevent="handleSubmit" class="password-form">
        <div class="form-group">
          <label class="form-label">현재 비밀번호</label>
          <input 
            v-model="formData.currentPassword"
            type="password"
            class="form-input"
            :class="{ 'error': errors.current_password }"
            required
          />
          <span v-if="errors.current_password" class="error-message">
            {{ errors.current_password }}
          </span>
        </div>

        <div class="form-group">
          <label class="form-label">새 비밀번호</label>
          <input 
            v-model="formData.newPassword"
            type="password"
            class="form-input"
            :class="{ 'error': errors.new_password }"
            required
          />
          <span v-if="errors.new_password" class="error-message">
            {{ errors.new_password }}
          </span>
        </div>

        <div class="form-group">
          <label class="form-label">새 비밀번호 확인</label>
          <input 
            v-model="formData.confirmPassword"
            type="password"
            class="form-input"
            :class="{ 'error': errors.confirm_password }"
            required
          />
          <span v-if="errors.confirm_password" class="error-message">
            {{ errors.confirm_password }}
          </span>
        </div>

        <div class="button-group">
          <button type="submit" class="submit-btn" :disabled="isLoading">
            {{ isLoading ? '변경중...' : '비밀번호 변경' }}
          </button>
          <button type="button" class="cancel-btn" @click="closeModal">
            취소
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['close'])
const userStore = useUserStore()

const formData = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const resetForm = () => {
  formData.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  errors.value = {}
}

const errors = ref({})
const isLoading = ref(false)

const validateForm = () => {
  errors.value = {}
  let isValid = true

  if (!formData.value.currentPassword) {
    errors.value.current_password = '현재 비밀번호를 입력해주세요.'
    isValid = false
  }

  if (!formData.value.newPassword) {
    errors.value.new_password = '새 비밀번호를 입력해주세요.'
    isValid = false
  }

  if (formData.value.newPassword.length < 8) {
    errors.value.new_password = '비밀번호는 8자 이상이어야 합니다.'
    isValid = false
  }

  if (formData.value.newPassword !== formData.value.confirmPassword) {
    errors.value.confirm_password = '새 비밀번호가 일치하지 않습니다.'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    isLoading.value = true
    const response = await axios.put(
      'http://127.0.0.1:8000/api/v1/users/password/change/',
      {
        current_password: formData.value.currentPassword,
        new_password: formData.value.newPassword
      },
      {
        headers: { Authorization: `Token ${userStore.token}` }
      }
    )

    alert('비밀번호가 성공적으로 변경되었습니다.')
    resetForm()
    emit('close')
  } catch (err) {
    console.error('비밀번호 변경 실패:', err)
    if (err.response?.data.error) {
      errors.value.current_password = err.response.data.error
    } else {
      errors.value.general = '비밀번호 변경 중 오류가 발생했습니다.'
    }
  } finally {
    isLoading.value = false
  }
}

const closeModal = () => {
  resetForm()
  emit('close')
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
  animation: slideUp 0.3s ease;
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

.modal-close {
  background: none;
  border: none;
  color: #c8c8c8;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: white;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
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
  transform: translateY(-2px);
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

/* 애니메이션 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

/* 반응형 디자인 */
@media (max-width: 768px) {
  .modal-content {
    padding: 1.5rem;
  }

  .button-group {
    flex-direction: column;
  }

  .submit-btn, .cancel-btn {
    width: 100%;
  }
}
</style>