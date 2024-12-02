import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useWishStore } from '@/stores/wishlist'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const movies = ref([])
  const wishStore = useWishStore()
  const currentMovie = ref(null)
  const error = ref(null)
  const isLoading = ref(false)
  const API_URL = 'http://127.0.0.1:8000'

  const token = localStorage.getItem('token')
  const config = {
    headers: {
      Authorization: token ? `Token ${token}` : null
    }
  }

  const fetchMovies = async () => {
    isLoading.value = true
    try {
      const response = await axios.get(`${API_URL}/api/v1/movies/movies/`, config)
      movies.value = response.data
    } catch (error) {
      console.error("영화 목록을 가져오는 데 실패했습니다:", error)
    } finally {
      isLoading.value = false
    }
  }

  const fetchMovieDetail = async (id) => {
    if (!id) {
      error.value = 'Movie ID is required'
      return
    }
    
    try {
      const response = await axios.get(`${API_URL}/api/v1/movies/${id}/`, config)
      currentMovie.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('영화 상세 정보 로딩 실패:', err)
    }
  }

  const platforms = ref([
    { name: 'NETFLIX', id: 'netflix', price: 13500, logo_path: "https://image.tmdb.org/t/p/original/pbpMk2JmcoNnQwx5JGpXngfoWtp.jpg" },
    { name: 'WAVVE', id: 'wavve', price: 10900, logo_path: "https://image.tmdb.org/t/p/original/hPcjSaWfMwEqXaCMu7Fkb529Dkc.jpg" },
    { name: 'DISNEY PLUS', id: 'disney', price: 9900, logo_path: "https://image.tmdb.org/t/p/original/97yvRBw1GzX7fXprcF80er19ot.jpg" },
    { name: 'WATCHA', id: 'watcha', price: 7900, logo_path: "https://image.tmdb.org/t/p/original/5gmEivxOGPdq4Afpq1f8ktLtEW1.jpg" }
  ])

  // wishStore의 찜 목록을 기반으로 플랫폼별 영화 분류
  const moviesByPlatform = computed(() => {
    const result = {}
    platforms.value.forEach(platform => {
      result[platform.id] = wishStore.movieWishlist.filter(movie =>
        movie.providers?.some(provider =>
          provider.name.toLowerCase() === platform.name.toLowerCase()
        )
      )
    })
    console.log('moviesByPlatform result:', result)
    console.log('wishStore movies:', wishStore.movieWishlist)
    return result
  })

  const recommendedPlatform = computed(() => {
    const platformCounts = platforms.value.map(platform => ({
      name: platform.name,
      count: moviesByPlatform.value[platform.id]?.length || 0,
      price: platform.price
    }))
    
    const maxCount = Math.max(...platformCounts.map(p => p.count))
  
    // 최대 개수를 가진 플랫폼들 중 가격이 가장 저렴한 것 선택
    return platformCounts
      .filter(p => p.count === maxCount)
      .sort((a, b) => a.price - b.price)[0].name
  })
  
  return {
    movies,
    isLoading,
    currentMovie,
    fetchMovies,
    fetchMovieDetail,
    error,
    platforms,
    moviesByPlatform,
    recommendedPlatform,
  }
}, {
  persist: true
}
)