<template>
  <div class="ott-section">
    <div class="platform-header">
      <img 
        :src="platform.logo_path" 
        :alt="`${platform.name} logo`"
        class="platform-logo"
      />
      <h2 class="platform-title">
        <template v-if="platform.id === 'disney'">
          DISNEY<span class="plus-symbol">+</span>
        </template>
        <template v-else>
          {{ platform.name }}
        </template>
      </h2>
    </div>
    <div class="content-box">
      <div class="wishlist-count">
        내가 찜한 영화 ({{ movies.length }})
      </div>
      <div class="movie-grid">
        <template v-if="movies.length">
          <div
            v-for="movie in movies" 
            :key="movie.movie_id" 
            class="movie-card"
            @click="goToDetail(movie.movie_id)"
          >
            {{ movie.title }}
          </div>
        </template>
        <div v-else class="empty-message">
          컨텐츠가 없습니다!
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

defineProps({
  platform: {
    type: Object,
    required: true
  },
  movies: {
    type: Array,
    required: true
  }
})

const router = useRouter()

const goToDetail = (movieId) => {
  router.push({ name: 'moviedetail', params: { id: movieId }})
}
</script>

<style scoped>
.ott-section {
  display: flex;
  flex-direction: column;
}

.platform-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  height: 48px;
}

.platform-logo {
  height: 32px;
  width: auto;
  object-fit: contain;
}

.platform-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(45deg, #ffffff 30%, #8346ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.content-box {
  border: 1px solid rgba(131, 70, 255, 0.3);
  border-radius: 16px;
  padding: 1.5rem;
  background: rgba(131, 70, 255, 0.05);
  height: 300px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.wishlist-count {
  text-align: center;
  font-size: 1rem;
  color: #f8f8f8;
  opacity: 0.9;
  margin-bottom: 1rem;
}

.movie-grid {
  text-align: center;
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
  overflow-y: auto;
  scrollbar-color: rgba(85, 85, 85, 0.5) transparent;
}

.movie-grid::-webkit-scrollbar {
  width: 8px;
}

.movie-grid::-webkit-scrollbar-track {
  background: transparent;
}

.movie-grid::-webkit-scrollbar-thumb {
  background: rgba(131, 70, 255, 0.5);
  border-radius: 4px;
}

.movie-grid::-webkit-scrollbar-thumb:hover {
  background: rgba(131, 70, 255, 0.7);
}

.movie-card {
  padding: 0.75rem 1rem;
  background: rgba(131, 70, 255, 0.1);
  border-radius: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 0.9rem;
  color: #f8f8f8;
}

.movie-card:hover {
  transform: translateY(-2px);
  background: rgba(131, 70, 255, 0.2);
  box-shadow: 0 4px 12px rgba(131, 70, 255, 0.2);
}

.empty-message {
  color: #8e8e8e;
  font-size: 0.9rem;
  text-align: center;
  padding: 2rem 0;
}
</style>