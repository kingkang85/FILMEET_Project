<template>
  <div class="poster-section">
    <div class="poster-container">
      <img :src="posterPath" :alt="title" class="poster-image" />
      <div v-if="videoPath" class="play-button hover-effect" @click="$emit('play')">
        <div class="play-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
          </svg>
        </div>
      </div>
    </div>
    <div class="genre-tags">
      <router-link 
        v-for="genre in genres"
        :key="genre.id"
        :to="{ name: 'movielist', query: { filter: 'genre', genreId: genre.genre_id }}"
        class="genre-tag hover-effect"
      >
        {{ genre.name }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({
  posterPath: String,
  title: String,
  videoPath: String,
  genres: Array
})

defineEmits(['play'])
</script>

<style scoped>
.poster-section {
  width: 350px;
  flex-shrink: 0;
}

.poster-container {
  position: relative;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background: #000;
}

.poster-image {
  width: 100%;
  display: block;
  transition: transform 0.3s ease;
}

.poster-container:hover .poster-image {
  transform: scale(1.05);
}

.play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid rgba(255, 255, 255, 0.8);
  color: white;
  z-index: 10;
}

.poster-container:hover .play-button {
  background: rgba(131, 70, 255, 0.8);
  box-shadow: 0 0 20px rgba(131, 70, 255, 0.5);
  border-color: transparent;
}

.play-icon {
  width: 24px;
  height: 24px;
  margin-left: 4px;
}

.play-button:hover {
  transform: translate(-50%, -50%) scale(1.1);
}

.genre-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.genre-tag {
  background: rgba(131, 70, 255, 0.15);
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 20px;
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 1px solid rgba(131, 70, 255, 0.3);
  backdrop-filter: blur(5px);
  position: relative;
  overflow: hidden;
}

.genre-tag::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    45deg,
    rgba(131, 70, 255, 0.2),
    rgba(79, 159, 255, 0.2)
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.genre-tag:hover {
  background: rgba(131, 70, 255, 0.25);
  transform: translateY(-2px);
  border-color: rgba(131, 70, 255, 0.5);
  box-shadow: 
    0 4px 12px rgba(131, 70, 255, 0.2),
    0 0 0 1px rgba(131, 70, 255, 0.1);
}

.genre-tag:hover::before {
  opacity: 1;
}

@media (max-width: 768px) {
  .poster-section {
    width: 100%;
  }
  
  .play-button {
    width: 60px;
    height: 60px;
  }
  
  .play-icon {
    width: 20px;
    height: 20px;
  }

  .genre-tags {
    justify-content: center;
    margin-top: 1rem;
  }

  .genre-tag {
    font-size: 0.85rem;
    padding: 0.4rem 1rem;
  }
}
.genre-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.genre-tag {
  background: rgba(131, 70, 255, 0.12);
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 20px;
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 1.5px solid rgba(131, 70, 255, 0.6); /* 테두리 두께와 투명도 조정 */
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 0 0 1px rgba(131, 70, 255, 0.2), /* 내부 그림자 */
    inset 0 0 0 1px rgba(131, 70, 255, 0.2); /* 내부 테두리 */
}

.genre-tag::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    45deg,
    rgba(131, 70, 255, 0.15),
    rgba(79, 159, 255, 0.15)
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.genre-tag:hover {
  background: rgba(131, 70, 255, 0.25);
  transform: translateY(-2px);
  border-color: rgba(131, 70, 255, 0.8); /* hover 시 테두리 색상 진하게 */
  box-shadow: 
    0 4px 12px rgba(131, 70, 255, 0.3),
    0 0 0 1.5px rgba(131, 70, 255, 0.4),
    inset 0 0 0 1px rgba(131, 70, 255, 0.3);
}

.genre-tag:hover::before {
  opacity: 1;
}

@media (max-width: 768px) {
  /* ... 기존 모바일 스타일 유지 ... */

  .genre-tag {
    font-size: 0.85rem;
    padding: 0.4rem 1rem;
    border-width: 1.5px; /* 모바일에서도 테두리 유지 */
  }
}
</style>