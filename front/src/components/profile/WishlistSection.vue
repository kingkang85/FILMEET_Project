<template>
  <div class="section-container">
    <div class="section-header">
      <h2 class="section-title">{{ user.nickname }}님이 {{ title }}</h2>
      <RouterLink :to="{ name: routeName }" class="see-more">
        See More
      </RouterLink>
    </div>

    <!-- 찜 목록이 있을 때 -->
    <div v-if="items.length > 0" class="movie-grid">
      <div v-for="item in items" :key="item.id" class="movie-card">
        <RouterLink :to="{ name: detailRouteName, params: { id: item[idKey] }}">
          <img :src="item[imageKey]" :alt="item[nameKey]" class="movie-poster" />
        </RouterLink>
        <div class="movie-title">{{ item[nameKey] }}</div>
      </div>
    </div>
    <!-- 찜 목록이 없을 때 -->
    <div v-else class="empty-state">
      <p>아직 {{ title }}이 없습니다.</p>
      <p class="empty-state-sub">관심있는 콘텐츠를 찜해보세요!</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  user: {
    type: Object,
    required: true
  },
  title: String,
  items: Array,
  routeName: String,
  detailRouteName: String,
  idKey: String,
  imageKey: String,
  nameKey: String
})
</script>

<style>
.section-container {
  margin-bottom: 4rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  color: white;
  margin: 0;
}

.see-more {
  color: #8346ff;
  font-family: "Inter-Regular", Helvetica;
  font-size: 1.2rem;
  text-decoration: none;
  transition: color 0.3s ease;
}

.see-more:hover {
  color: #9666ff;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

.movie-card {
  position: relative;
  transition: transform 0.2s;
}

.movie-card:hover {
  transform: scale(1.05);
}

.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.movie-title {
  margin-top: 0.5rem;
  text-align: center;
  color: white;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .movie-poster {
    height: 225px;
  }
  
  .section-title {
    font-size: 1.2rem;
  }
  
  .see-more {
    font-size: 1rem;
  }
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: rgba(131, 70, 255, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(131, 70, 255, 0.2);
}

.empty-state p {
  color: white;
  font-size: 1.2rem;
  margin: 0;
}

.empty-state-sub {
  color: #c8c8c8 !important;
  font-size: 1rem !important;
  margin-top: 0.5rem !important;
}
</style>