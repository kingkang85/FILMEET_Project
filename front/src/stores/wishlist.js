import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from '@/stores/user'  // userStore import 추가

export const useWishStore = defineStore('wish', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const userStore = useUserStore()  // userStore 초기화
  
  const movieWishlist = ref([])
  const actorWishlist = ref([])
  const directorWishlist = ref([])
  
  // 헤더 가져오는 함수 추가
  const getHeaders = () => ({
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
  
  // computed 속성들은 그대로 유지
  const isMovieInWishlist = computed(() => (movieId) => {
    return movieWishlist.value.some(movie => movie.movie_id === movieId)
  })

  const isActorInWishlist = computed(() => (actorId) => {
    return actorWishlist.value.some(actor => actor.person_id === actorId)
  })

  const isDirectorInWishlist = computed(() => (directorId) => {
    return directorWishlist.value.some(director => director.person_id === directorId)
  })

  // 영화 찜 토글 함수 수정
  const toggleMovieWish = async (movieId) => {
    if (!userStore.isLoggedIn) {
      throw new Error('User must be logged in')
    }

    try {
      if (isMovieInWishlist.value(movieId)) {
        await axios.delete(
          `${API_URL}/api/v1/movies/${movieId}/wishlist/`, 
          getHeaders()
        )
      } else {
        await axios.post(
          `${API_URL}/api/v1/movies/${movieId}/wishlist/`, 
          null, 
          getHeaders()
        )
      }
      await getMovieWishlist()
      return true
    } catch (err) {
      console.error('위시리스트 토글 실패:', err)
      throw err
    }
  }

  // 영화 찜하기 함수 수정
  const wishMovie = async (movieId) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/v1/movies/${movieId}/wishlist/`,
        null,
        getHeaders()
      )
      await getMovieWishlist()
      return response.data.status
    } catch (err) {
      console.error('영화 찜하기 실패:', err)
      throw err
    }
  }

  // 영화 찜 목록 가져오기 함수 수정
  const getMovieWishlist = async () => {
    if (!userStore.isLoggedIn) {
      movieWishlist.value = []
      return
    }

    try {
      const response = await axios.get(
        `${API_URL}/api/v1/movies/wishlist/`, 
        getHeaders()
      )
      movieWishlist.value = response.data
    } catch (err) {
      console.error('영화 위시리스트 조회 실패:', err)
      throw err
    }
  }

  // 배우 찜하기 함수 수정
  const wishActor = async (actorId) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/v1/movies/actors/${actorId}/wishlist/`,
        null,
        getHeaders()
      )
      await getActorWishlist()
      return response.data.status
    } catch (err) {
      console.error('배우 찜하기 실패:', err)
      throw err
    }
  }

  // 배우 찜 목록 가져오기 함수 수정
  const getActorWishlist = async () => {
    if (!userStore.isLoggedIn) {
      actorWishlist.value = []
      return
    }

    try {
      const response = await axios.get(
        `${API_URL}/api/v1/movies/actors/wishlist/`, 
        getHeaders()
      )
      actorWishlist.value = response.data
    } catch (err) {
      console.error('배우 위시리스트 조회 실패:', err)
      throw err
    }
  }

  // 감독 찜하기 함수 수정
  const wishDirector = async (directorId) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/v1/movies/directors/${directorId}/wishlist/`,
        null,
        getHeaders()
      )
      await getDirectorWishlist()
      return response.data.status
    } catch (err) {
      console.error('감독 찜하기 실패:', err)
      throw err
    }
  }

  // 감독 찜 목록 가져오기 함수 수정
  const getDirectorWishlist = async () => {
    if (!userStore.isLoggedIn) {
      directorWishlist.value = []
      return
    }

    try {
      const response = await axios.get(
        `${API_URL}/api/v1/movies/directors/wishlist/`, 
        getHeaders()
      )
      directorWishlist.value = response.data
    } catch (err) {
      console.error('감독 위시리스트 조회 실패:', err)
      throw err
    }
  }

  return { 
    movieWishlist,
    wishMovie,
    getMovieWishlist,
    toggleMovieWish,
    isMovieInWishlist,
    actorWishlist,
    wishActor,
    getActorWishlist,
    isActorInWishlist,
    directorWishlist,
    wishDirector,
    getDirectorWishlist,
    isDirectorInWishlist
  }
})