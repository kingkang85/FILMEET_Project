<script setup>
import { ref, onMounted, computed } from 'vue'
import { useWishStore } from '@/stores/wishlist'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import router from '@/router'

const props = defineProps({
  winner: {
    type: Object,
    required: true
  }
})

defineEmits(['restart'])

const userStore = useUserStore()
const wishStore = useWishStore()
const actorMovies = ref([])
const error = ref(null)

// 헤더 가져오기
const getHeaders = () => {
  const token = userStore.token
  if (!token) return null
  return {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json',
    }
  }
}

// 위시리스트 상태 체크
const isWished = computed(() => 
  props.winner?.person_id ? wishStore.isActorInWishlist(props.winner.person_id) : false
)

const isMovieWished = (movieId) => 
  movieId ? wishStore.isMovieInWishlist(movieId) : false

// API 호출
const fetchActorMovies = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/movies/actors/${props.winner.person_id}/`)
    actorMovies.value = response.data.filmography || []
  } catch (err) {
    error.value = err.message
    console.error('Error fetching actor movies:', err)
  }
}

const toggleWishActor = async () => {
  try {
    const headers = getHeaders()
    if (!headers) {
      alert('로그인이 필요한 서비스입니다!')
      return
    }

    await axios.post(
      `http://127.0.0.1:8000/api/v1/movies/actors/${props.winner.person_id}/wishlist/`,
      {},
      headers
    )
    await wishStore.getActorWishlist()
  } catch (err) {
    console.error('Error toggling actor wish:', err)
    if (err.response?.status === 401) {
      alert('로그인이 필요한 서비스입니다.')
    }
  }
}

const toggleWishMovie = async (movieId) => {
  try {
    const headers = getHeaders()
    if (!headers) {
      alert('로그인이 필요한 서비스입니다!')
      return
    }

    await axios.post(
      `http://127.0.0.1:8000/api/v1/movies/${movieId}/wishlist/`,
      {},
      headers
    )
    await wishStore.getMovieWishlist()
  } catch (err) {
    console.error('Error toggling movie wish:', err)
    if (err.response?.status === 401) {
      alert('로그인이 필요한 서비스입니다.')
    }
  }
}

onMounted(() => {
  if (props.winner?.person_id) {
    fetchActorMovies()
  }
})
</script>

<template>
  <div class="result-container">
    <h2>우승자</h2>
    <div v-if="winner" class="winner-card">
      <img 
        :src="winner.profile_path" 
        :alt="winner.name"
        @error="$event.target.src = '/default-profile.jpg'"
      >
      <div class="winner-info">
        <div class="winner-name">{{ winner.name }}</div>
        <button 
          @click="toggleWishActor"
          :class="['wish-button', { 'wished': isWished }]"
        >
          {{ isWished ? '찜 해제' : '찜하기' }}
        </button>
      </div>
    </div>

    <div v-if="actorMovies.length" class="movies-section">
      <h3>출연 영화</h3>
      <div class="movies-grid">
        <div 
          v-for="movie in actorMovies" 
          :key="movie.movie_id" 
          class="movie-card"
        >
          <img 
            :src="movie.poster_path" 
            :alt="movie.title"
            @error="$event.target.src = '/default-poster.jpg'"
          >
          <div class="movie-info">
            <div class="movie-title">{{ movie.title }}</div>
            <button 
              @click="toggleWishMovie(movie.movie_id)"
              :class="['wish-button', { 'wished': isMovieWished(movie.movie_id) }]"
            >
              {{ isMovieWished(movie.movie_id) ? '찜 해제' : '찜하기' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <button @click="$emit('restart')" class="restart-button">
      다시 하기
    </button>
  </div>
</template>

<style scoped>
.result-container {
  text-align: center;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  color: white;
}

h2, h3 {
  color: white;
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: 600;
  background: linear-gradient(45deg, #935dff, #4f9fff);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -1px;
}

.winner-card {
  max-width: 400px;
  margin: 2rem auto;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.winner-card:hover {
  transform: translateY(-5px);
}

.winner-card img {
  width: 100%;
  height: 500px;
  object-fit: cover;
}

.winner-info {
  padding: 1.5rem;
}

.winner-name {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: white;
}

.movies-section {
  margin: 4rem auto;
  max-width: 1000px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, 200px);
  gap: 1.5rem;
  justify-content: center;
  width: 100%;
}

.movie-card {
  width: 200px;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.2);
  transition: all 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(131, 70, 255, 0.2);
}

.movie-card img {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
}

.movie-info {
  padding: 0.8rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 0.3rem auto;
}

.movie-title {
  font-size: 1rem;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 0.3rem;
  margin-bottom: 0.3rem;
}

.wish-button {
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  background: linear-gradient(45deg, #8346ff, #4f9fff);
  border: none;
  border-radius: 20px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  width: auto;
  align-self: center;
}

.wish-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(131, 70, 255, 0.3);
}

.wish-button.wished {
  background: linear-gradient(45deg, #4f9fff, #8346ff);
}

.restart-button {
  padding: 1rem 2.5rem;
  font-size: 1.2rem;
  background: linear-gradient(45deg, #8346ff, #4f9fff);
  border: none;
  border-radius: 30px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.restart-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 20px rgba(131, 70, 255, 0.4);
}

@media (max-width: 768px) {
  .movies-grid {
    grid-template-columns: repeat(auto-fit, 150px);  /* 모바일에서는 더 작은 크기로 */
    gap: 1rem;
  }

  .movie-card {
    width: 150px;
  }
}

@media (max-width: 480px) {
  .movies-grid {
    grid-template-columns: repeat(auto-fit, 130px);
    gap: 0.8rem;
  }

  .movie-card {
    width: 130px;
  }
}
</style>