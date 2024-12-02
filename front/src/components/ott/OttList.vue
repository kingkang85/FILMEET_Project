<template>
  <div class="ott-grid">
    <OttListItem
      v-for="platform in movieStore.platforms"
      :key="platform.name"
      :platform="platform"
      :movies="movieStore.moviesByPlatform[platform.id]"
    />
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie'
import OttListItem from '@/components/ott/OttListItem.vue'

const movieStore = useMovieStore()
</script>

<style scoped>
.ott-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  margin-bottom: 4rem;
}

@media (max-width: 1200px) {
  .ott-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .ott-grid {
    grid-template-columns: 1fr;
  }
}
</style>