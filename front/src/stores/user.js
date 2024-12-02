import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

export const useUserStore = defineStore('user', () => {
  // 상태 정의
  const user = ref(null)
  const token = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const showEndingCredits = ref(false)

  // computed
  const isLoggedIn = computed(() => !!token.value)
  const getUser = computed(() => user.value)
  const getError = computed(() => error.value)

  // 회원가입 함수
  const register = (userData) => {
    isLoading.value = true
    error.value = null
    
    const form = new FormData()
    
    // 필수 필드
    form.append('username', userData.username)
    form.append('password1', userData.password1)
    form.append('password2', userData.password2)
    form.append('nickname', userData.nickname)
    form.append('email', userData.email)
    
    // 선택적 필드
    if (userData.phone_num) form.append('phone_num', userData.phone_num)
    if (userData.birth_date) form.append('birth_date', userData.birth_date)
    if (userData.profile_image) form.append('profile_image', userData.profile_image)

    return axios.post(`${API_URL}/accounts/signup/`, form, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    })
      .then((response) => {
        return response.data
      })
      .catch((err) => {
        console.error('회원가입 에러:', err.response?.data)
        error.value = err.response?.data || { message: '회원가입 중 오류가 발생했습니다.' }
        throw err
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  // 로그인 함수
  const login = (credentials) => {
    isLoading.value = true
    error.value = null

    return axios.post(`${API_URL}/accounts/login/`, credentials)
      .then((response) => {
        token.value = response.data.key
        return getUserInfo().then(() => response.data)
      })
      .catch((err) => {
        error.value = err.response?.data || { message: '로그인 중 오류가 발생했습니다.' }
        throw err
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  // 사용자 정보 조회
  const getUserInfo = () => {
    if (!token.value) return Promise.resolve(null)

    return axios.get(`${API_URL}/api/v1/users/profile/`, {
      headers: { Authorization: `Token ${token.value}` }
    })
      .then((response) => {
        user.value = response.data
        return response.data
      })
      .catch((err) => {
        console.error('프로필 조회 실패:', err)
        throw err
      })
  }

  // 로그아웃
  const logout = () => {
    isLoading.value = true
    error.value = null

    return axios.post(`${API_URL}/accounts/logout/`)
      .then(() => {
        user.value = null
        token.value = null
      })
      .catch((err) => {
        console.error('로그아웃 실패:', err)
        throw err
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  // 회원 탈퇴
  const resign = () => {
    isLoading.value = true
    error.value = null

    return axios.delete(`${API_URL}/api/v1/users/delete/`, {
      headers: { Authorization: `Token ${token.value}` }
    })
      .then(() => {
        showEndingCredits.value = true
        
        setTimeout(() => {
          user.value = null
          token.value = null
          showEndingCredits.value = false
        }, 20000)
      })
      .catch((err) => {
        console.error('회원 탈퇴 실패:', err)
        error.value = err.response?.data || { message: '회원 탈퇴 중 오류가 발생했습니다.' }
        throw err
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  // 회원 정보 수정
  const update = (userData) => {
    isLoading.value = true
    error.value = null

    const form = new FormData()

    if (userData.nickname) form.append("nickname", userData.nickname)
    if (userData.phone_num) form.append("phone_num", userData.phone_num)
    if (userData.birth_date) form.append("birth_date", userData.birth_date)
    if (userData.profile_image) form.append("profile_image", userData.profile_image)

    return axios.put(`${API_URL}/api/v1/users/update/`, form, {
      headers: { 
        Authorization: `Token ${token.value}`,
        "Content-Type": "multipart/form-data"
      }
    })
      .then((response) => {
        return getUserInfo().then(() => response.data)
      })
      .catch((err) => {
        console.error('정보 수정 실패:', err)
        error.value = err.response?.data || {message: '정보 수정 중 오류가 발생했습니다.'}
        throw err
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  return {
    // 상태
    user,
    token,
    isLoading,
    error,
    showEndingCredits,
    
    // computed
    isLoggedIn,
    getUser,
    getError,
    
    // 메소드
    register,
    login,
    getUserInfo,
    logout,
    resign,
    update
  }
}, {
  persist: true
})