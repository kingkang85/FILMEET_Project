// stores/community.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export const useCommunityStore = defineStore('community', () => {
  const API_URL = 'http://127.0.0.1:8000'  // API_URL 추가
  const userStore = useUserStore()
  
  // 상태 관리
  const discussions = ref([])
  const currentPage = ref(1)
  const totalPages = ref(1)
  const isLoading = ref(false)
  const error = ref(null)

  // 헤더 설정
  const getHeaders = () => {
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
  }

  // 댓글 정렬 (내 댓글/다른 사람 댓글 구분)
  const sortedDiscussions = computed(() => {
    if (!discussions.value || !Array.isArray(discussions.value)) {
      return {
        myDiscussions: [],
        otherDiscussions: []
      }
    }

    const currentUserId = userStore.user?.id

    const sortedArray = [...discussions.value].sort(
      (a, b) => new Date(a.created_at) - new Date(b.created_at)
    )
    
    const myDiscussions = sortedArray.filter(
      discussion => discussion.user?.id === currentUserId
    )
    
    const otherDiscussions = sortedArray.filter(
      discussion => discussion.user?.id !== currentUserId
    )
    
    return {
      myDiscussions,
      otherDiscussions
    }
  })

  // 댓글 목록 조회
  const fetchDiscussions = async (movieId, page = 1) => {
    if (!movieId) return
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await axios.get(
        `${API_URL}/api/v1/community/movies/${movieId}/discussions/?page=${page}&ordering=created_at`,
        getHeaders()
      )
      
      discussions.value = response.data.results
      totalPages.value = Math.ceil(response.data.count / 10)  
      currentPage.value = page

      discussions.value = discussions.value.map(d => ({
        ...d,
        showContent: false
      }))

    } catch (err) {
      console.error('Error fetching discussions:', err)
      error.value = err.response?.data?.detail || '댓글을 불러오는데 실패했습니다.'
      throw err
    } finally {
      isLoading.value = false
    }
  }

 // 댓글 작성
 const createDiscussion = async (movieId, content) => {
   if (!movieId || !content) return
   
   error.value = null
   try {
     const response = await axios.post(
       `http://127.0.0.1:8000/api/v1/community/movies/${movieId}/discussions/`,
       {
         content,
         movie: movieId,
       },
       getHeaders()
     )
     
     // 새 댓글 추가
     discussions.value = [...discussions.value, response.data]
     return response.data
     
   } catch (err) {
     error.value = err.response?.data?.detail || '댓글 작성에 실패했습니다.'
     throw err
   }
 }

 // 댓글 수정
 const updateDiscussion = async (discussionId, content) => {
   if (!discussionId || !content) return
   
   error.value = null
   try {
     const response = await axios.put(
       `http://127.0.0.1:8000/api/v1/community/discussions/${discussionId}/`,
       { content },
       getHeaders()
     )

     // 수정된 댓글 반영
     const index = discussions.value.findIndex(d => d.id === discussionId)
     if (index !== -1) {
       discussions.value[index] = response.data
     }
     return response.data
     
   } catch (err) {
     error.value = err.response?.data?.detail || '댓글 수정에 실패했습니다.'
     throw err
   }
 }

 // 댓글 삭제
 const deleteDiscussion = async (discussionId) => {
   if (!discussionId) return
   
   error.value = null
   try {
     await axios.delete(
       `http://127.0.0.1:8000/api/v1/community/discussions/${discussionId}/`,
       getHeaders()
     )
     
     // 삭제된 댓글 제거
     discussions.value = discussions.value.filter(d => d.id !== discussionId)
     
   } catch (err) {
     error.value = err.response?.data?.detail || '댓글 삭제에 실패했습니다.'
     throw err
   }
 }

 // 댓글 신고
 const reportDiscussion = async (discussionId, reportData) => {
   if (!discussionId) return
   
   error.value = null
   try {
     const response = await axios.post(
       `http://127.0.0.1:8000/api/v1/community/discussions/${discussionId}/report/`,
       reportData,
       getHeaders()
     )

     // 신고된 댓글 상태 업데이트
     const index = discussions.value.findIndex(d => d.id === discussionId)
     if (index !== -1) {
       discussions.value[index] = {
         ...discussions.value[index],
         is_reported: true,
         report_count: discussions.value[index].report_count + 1
       }
     }
     return response.data
     
   } catch (err) {
     error.value = err.response?.data?.detail || '신고 처리에 실패했습니다.'
     throw err
   }
 }

 // 댓글 목록 초기화
 const clearDiscussions = () => {
   discussions.value = []
   error.value = null
   currentPage.value = 1
   totalPages.value = 1
 }

 return {
   discussions,
   isLoading,
   error,
   currentPage, 
   totalPages,
   sortedDiscussions,
   fetchDiscussions,
   createDiscussion,
   updateDiscussion, 
   deleteDiscussion,
   clearDiscussions,
   reportDiscussion,
 }
})