<!-- src/components/MovieCard.vue -->
<template>
  <div class="movie-card">
    <div class="movie-poster">
      <img 
        :src="movie.poster_path" 
        :alt="movie.title"
        @error="$emit('imageError', $event)"
      >
      <div class="movie-rating">
        <span class="star">★</span>
        {{ movie.vote_average.toFixed(1) }}
      </div>
    </div>
    <div class="movie-info">
      <h4>{{ movie.title }}</h4>
      <p class="overview">{{ movie.overview }}</p>
      <div class="movie-meta">
        <div class="meta-item">
          <span class="meta-label">개봉</span>
          <span>{{ formatDate(movie.release_date) }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">장르</span>
          <span>{{ formatGenres(movie.genres) }}</span>
        </div>
        <div v-if="movie.runtime" class="meta-item">
          <span class="meta-label">상영시간</span>
          <span>{{ formatRuntime(movie.runtime) }}</span>
        </div>
      </div>
      <div class="action-buttons">
        <button 
          class="detail-btn primary" 
          @click="$emit('viewDetail')"
        >
          상세 정보
        </button>
        <button 
          class="wishlist-btn"
          :class="{ 'in-wishlist': isInWishlist }"
          @click="$emit('toggleWishlist')"
        >
          <span class="icon">{{ isInWishlist ? '★' : '☆' }}</span>
          {{ isInWishlist ? '찜됨' : '찜하기' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { format } from 'date-fns'
import { ko } from 'date-fns/locale'

const props = defineProps({
  movie: {
    type: Object,
    required: true
  },
  isInWishlist: {
    type: Boolean,
    default: false
  }
})

const formatDate = (date) => {
  try {
    return format(new Date(date), 'yyyy년 M월 d일', { locale: ko })
  } catch {
    return '날짜 정보 없음'
  }
}

const formatRuntime = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  return `${hours}시간 ${remainingMinutes}분`
}

const formatGenres = (genres) => {
  return genres?.map(g => g.name).join(', ') || '장르 정보 없음'
}
</script>

<style scoped>
.movie-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-2px);
}

.movie-poster {
  position: relative;
}

.movie-poster img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.movie-rating {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.star {
  color: #ffd700;
}

.movie-info {
  padding: 1rem;
}

.movie-info h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  margin-bottom: 0.5rem;
}

.overview {
  color: #ddd;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.movie-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #888;
}

.meta-label {
  color: #666;
  width: 5rem;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.detail-btn,
.wishlist-btn {
  flex: 1;
  padding: 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detail-btn {
  background: #8346ff;
  color: white;
  border: none;
}

.detail-btn:hover {
  background: #9666ff;
}

.wishlist-btn {
  background: transparent;
  border: 1px solid #8346ff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
}

.wishlist-btn:hover {
  background: rgba(131, 70, 255, 0.1);
}

.wishlist-btn.in-wishlist {
  background: rgba(255, 215, 0, 0.1);
  border-color: #ffd700;
  color: #ffd700;
}

.icon {
  font-size: 1rem;
}
</style>