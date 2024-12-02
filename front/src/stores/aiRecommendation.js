import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export const useAIRecommendationStore = defineStore('aiRecommendation', {
  state: () => ({
    error: null,
    isAIAvailable: true,
    excludeWishlisted: JSON.parse(localStorage.getItem('excludeWishlisted') || 'false'),
    API_URL: 'http://127.0.0.1:8000'  // API URL 추가
  }),
  
  actions: {
    getHeaders() {
      const userStore = useUserStore()
      const token = userStore.token
      if (!token) {
        throw new Error('Authentication token is missing')
      }
      return {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        }
      }
    },

    async getRecommendation(userInput, { excludeMovieIds = [] } = {}) {
      try {
        if (!this.isAIAvailable) {
          return this.getFallbackRecommendation(userInput, excludeMovieIds)
        }
        
        const response = await axios.post(
          `${this.API_URL}/api/v1/ai/recommend/`,  // API_URL 사용
          { 
            user_input: userInput,
            excludeWishlisted: this.excludeWishlisted ? excludeMovieIds : []
          },
          this.getHeaders()
        )
        this.error = null
        return response.data
      } catch (error) {
        if (error.response?.data?.code === 'ALL_MOVIES_WISHLISTED') {
          this.error = error.response.data.error
          return {
            error: error.response.data.error,
            suggestion: error.response.data.suggestion,
            code: 'ALL_MOVIES_WISHLISTED'
          }
        }

        if (error.response?.status === 429) {
          this.isAIAvailable = false
          return this.getFallbackRecommendation(userInput, excludeMovieIds)
        }

        if (error.response?.status === 500) {
          return this.getFallbackRecommendation(userInput, excludeMovieIds)
        }

        throw error
      }
    },
    
    async getFallbackRecommendation(userInput, excludeMovieIds = []) {
      try {
        const response = await axios.post(
          `${this.API_URL}/api/v1/ai/recommend/fallback/`,  // API_URL 사용
          { 
            user_input: userInput,
            excludeWishlisted: this.excludeWishlisted ? excludeMovieIds : []
          },
          this.getHeaders()
        )

        if (response.data?.code === 'ALL_MOVIES_WISHLISTED') {
          this.error = response.data.error
          return {
            error: response.data.error,
            suggestion: response.data.suggestion,
            code: 'ALL_MOVIES_WISHLISTED'
          }
        }

        return {
          ...response.data,
          note: this.isAIAvailable ? null : '현재 AI 서비스가 많이 사용되어 키워드 기반으로 추천해드렸습니다.'
        }
      } catch (error) {
        if (error.response?.data?.code === 'ALL_MOVIES_WISHLISTED') {
          this.error = error.response.data.error
          return {
            error: error.response.data.error,
            suggestion: error.response.data.suggestion,
            code: 'ALL_MOVIES_WISHLISTED'
          }
        }

        this.error = '영화 추천 서비스를 이용할 수 없습니다.'
        throw error
      }
    },

    setExcludeWishlisted(value) {
      this.excludeWishlisted = value
      localStorage.setItem('excludeWishlisted', JSON.stringify(value))
    },

    resetAIAvailability() {
      this.isAIAvailable = true
      this.error = null
    }
  }
})