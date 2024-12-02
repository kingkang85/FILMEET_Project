<template>
  <div class="movie-grid">
    <router-link
      v-for="movie in movies"
      :key="movie.movie_id"
      :to="{ name: 'moviedetail', params: { id: movie.movie_id }}"
      class="movie-card"
    >
      <div class="poster-container">
        <img 
          :src="movie.poster_path" 
          :alt="movie.title"
          class="poster-image"
        />
        <div class="poster-overlay">
          <div class="movie-info">
            <p class="release-date">{{ formatDate(movie.release_date) }}</p>
            <p v-if="showCharacter" class="character-name">
              {{ movie.character_name }}
            </p>
          </div>
        </div>
      </div>
      <h4 class="movie-title">{{ movie.title }}</h4>
    </router-link>
  </div>
</template>

<script setup>
const props = defineProps({
  movies: {
    type: Array,
    required: true
  },
  showCharacter: {
    type: Boolean,
    default: false
  }
})

const formatDate = (dateString) => {
  if (!dateString) return '정보 없음'
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.movie-card {
  text-decoration: none;
  color: white;
  transition: transform 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.poster-container {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 2/3;
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.movie-card:hover .poster-image {
  transform: scale(1.1);
}

.poster-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.movie-card:hover .poster-overlay {
  opacity: 1;
}

.movie-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  text-align: center;
}

.release-date {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.character-name {
  color: #a78bfa;
  font-size: 0.875rem;
}

.movie-title {
  margin-top: 0.75rem;
  text-align: center;
  font-weight: 500;
  transition: color 0.3s ease;
}

.movie-card:hover .movie-title {
  color: #a78bfa;
}

@media (max-width: 1024px) {
  .movie-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 768px) {
  .movie-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 640px) {
  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>