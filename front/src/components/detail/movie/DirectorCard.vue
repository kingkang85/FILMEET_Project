// components/movie/DirectorCard.vue
<template>
  <div class="director-section">
    <h3 class="director-title">감독</h3>
    <div class="director-card">
      <div class="image-wrapper">
        <img 
          :src="getImageUrl(director.profile_path)"
          :alt="director.name" 
          class="director-image" 
        />
        <div class="image-overlay"></div>
      </div>
      <p class="director-name">{{ director.name }}</p>
      <router-link 
        :to="{ name: 'directordetail', params: { id: director.person_id }}"
        class="more-btn"
      >
        <span>작품 더 보러가기</span>
        <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
        </svg>
      </router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({
  director: {
    type: Object,
    required: true
  }
})

const baseURL = 'http://127.0.0.1:8000'

const getImageUrl = (imagePath) => {
  // TMDB 이미지인 경우 (http로 시작하는 전체 URL)
  if (imagePath?.startsWith('http')) {
    return imagePath
  }
  // 이미지가 없는 경우 기본 이미지 반환
  return baseURL + '/static/images/default_profile.jpg'
}
</script>

<style scoped>
.director-section {
  width: 250px;
  flex-shrink: 0;
}

.director-title {
  font-size: 1.25rem;
  color: #a78bfa;
  margin-bottom: 1rem;
  font-weight: 600;
}

.director-card {
  background: rgba(255, 255, 255, 0.05);
  padding: 1.5rem;
  border-radius: 16px;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.director-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 20px rgba(131, 70, 255, 0.2);
}

.image-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.director-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.3) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.director-card:hover .director-image {
  transform: scale(1.1);
}

.director-card:hover .image-overlay {
  opacity: 1;
}

.director-name {
  font-size: 1.25rem;
  font-weight: 500;
  color: white;
  margin: 0.5rem 0 1rem;
}

.more-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #a78bfa;
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

.more-btn:hover {
  color: #d8b4fe;
  background: rgba(131, 70, 255, 0.1);
}

.arrow-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.more-btn:hover .arrow-icon {
  transform: translateX(4px);
}

@media (max-width: 1200px) {
  .director-section {
    width: 100%;
    max-width: 350px;
  }
}
</style>
