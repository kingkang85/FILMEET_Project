<template>
  <div class="movie-detail">
    <NavBar />
     <Transition name="fade">
      <div v-if="showTrailer" class="trailer-modal" @click.self="closeTrailer">
        <div class="trailer-container">
          <button class="close-modal" @click="closeTrailer">×</button>
          <div class="video-wrapper">
            <iframe
              :src="movie?.video_path"
              frameborder="0"
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Loading State -->
    <LoadingState v-if="isLoading" />
    
    <!-- Content -->
    <div v-else-if="movie" class="content-container">
      <div class="movie-main">
        <MoviePoster
          :poster-path="movie.poster_path"
          :title="movie.title"
          :video-path="movie.video_path"
          :genres="movie.genres"
          @play="showTrailer = true"
        />

        <MovieInfo
          :title="movie.title"
          :overview="movie.overview"
          :release-date="movie.release_date"
          :runtime="movie.runtime"
          :vote-average="movie.vote_average"
          :providers="movie.providers"
          :is-wished="isWished"
          @wish="handleWish"
          @discuss="showDiscussionModal = true"
        />

        <DirectorCard
          v-if="movie.director?.length"
          :director="movie.director[0]"
        />
      </div>

      <CastSection :cast="movie.cast" />
    </div>

    <!-- Error State -->
    <ErrorState 
      v-else 
      message="영화 정보를 찾을 수 없습니다."
    />

    <DiscussionModal 
      :is-open="showDiscussionModal"
      :movie-id="Number(route.params.id)"
      @close="closeDiscussionModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import { useWishStore } from '@/stores/wishlist'


// Components
import NavBar from '@/components/common/NavBar.vue'
import LoadingState from '@/components/detail/LoadingState.vue'
import ErrorState from '@/components/detail/ErrorState.vue'
import MoviePoster from '@/components/detail/movie/MoviePoster.vue'
import MovieInfo from '@/components/detail/movie/MovieInfo.vue'
import DirectorCard from '@/components/detail/movie/DirectorCard.vue'
import CastSection from '@/components/detail/movie/CastSection.vue'
import DiscussionModal from '@/components/DiscussionModal.vue'

const route = useRoute()
const router = useRouter()
const movieStore = useMovieStore()
const wishStore = useWishStore()

const isLoading = ref(true)
const showTrailer = ref(false)
const showDiscussionModal = ref(false)
const error = ref(null)

const movie = computed(() => movieStore.currentMovie)

const fetchMovieData = async () => {
  try {
    isLoading.value = true
    error.value = null
    await movieStore.fetchMovieDetail(route.params.id)
  } catch (err) {
    error.value = err.message
    console.error('Error fetching movie details:', err)
  } finally {
    isLoading.value = false
  }
}


// Modal Close Handler
const closeDiscussionModal = () => {
  showDiscussionModal.value = false
}

const closeTrailer = () => {
  showTrailer.value = false
}

const handleWish = async () => {
  if (!movie.value) return

  try {
    const status = await wishStore.wishMovie(movie.value.movie_id)
    if (status === 'added') {
      alert('찜 목록에 추가되었습니다.')
    } else {
      alert('찜 목록에서 제거되었습니다.')
    }
  } catch (err) {
    console.log(err)
    if (err.response?.status === 401) {
      alert('로그인이 필요합니다.')
      router.push('/login')
    }
  }
}

onMounted(async () => {
  if (route.params.id) {
    try {
      await Promise.all([
        fetchMovieData(),
        wishStore.getMovieWishlist()
      ])
    } catch (err) {
      console.error('Error initializing data:', err)
    }
  }
})

const isWished = computed(() => {
  if (!movie.value?.movie_id) return false
  return wishStore.isMovieInWishlist(movie.value.movie_id)
})

watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      fetchMovieData()
    }
  }
)
</script>

<style scoped>

/* 기존 스타일에 트랜지션 스타일 추가 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.movie-detail {
  min-height: 100vh;
  /* background: linear-gradient(135deg, #0b001a 0%, #2a1458 100%); */
  color: white;
  background-color: #0b001a;
  
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  animation: fadeIn 0.6s ease-out;
  background-color: #0b001a;
}

.movie-main {
  display: flex;
  gap: 3rem;
  margin-bottom: 4rem;
  background-color: #0b001a;
}

.trailer-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.trailer-container {
  position: relative;
  width: 90%;
  max-width: 1000px;
  margin: 2rem;
}

.video-wrapper {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.close-modal {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.close-modal:hover {
  transform: scale(1.1) rotate(90deg);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 1200px) {
  .movie-main {
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 640px) {
  .content-container {
    padding: 1rem;
  }

  .trailer-container {
    width: 95%;
    margin: 1rem;
  }
}
</style>