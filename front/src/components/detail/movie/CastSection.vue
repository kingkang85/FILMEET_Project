<template>
  <section class="cast-section">
    <div class="section-header">
      <h2 class="section-title">MOVIE INFO</h2>
    </div>

    <div class="actors-section">
      <h3 class="subsection-title">ACTOR</h3>
      <div class="actors-grid">
        <router-link 
          v-for="actor in cast" 
          :key="actor.id"
          :to="{ name: 'actordetail', params: { id: actor.id }}"
          class="actor-card"
        >
          <div class="card-content">
            <div class="image-wrapper">
              <img 
                :src="getImageUrl(actor.profile_path)"
                :alt="actor.name" 
                class="actor-image"
              />
              <div class="image-overlay">
                <span class="view-profile">프로필 보기</span>
              </div>
            </div>
            <div class="actor-info">
              <p class="actor-name">{{ actor.name }}</p>
              <p class="character-name">{{ actor.character_name }}</p>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  cast: {
    type: Array,
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
.cast-section {
  margin-top: 3rem;
}

.section-header {
  margin-bottom: 2rem;
  position: relative;
}

.section-header::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(to right, #8346ff33, transparent);
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  background: linear-gradient(to right, white, #a78bfa);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.subsection-title {
  font-size: 1.5rem;
  color: #a78bfa;
  margin-bottom: 1.5rem;
}

.actors-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1.5rem;
}

.actor-card {
  text-decoration: none;
  color: inherit;
}

.card-content {
  transition: transform 0.3s ease;
}

.actor-card:hover .card-content {
  transform: translateY(-5px);
}

.image-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 1;
  margin-bottom: 0.75rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.actor-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  display: flex;
  align-items: flex-end;
  padding: 1rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.view-profile {
  color: white;
  font-size: 0.875rem;
  transform: translateY(10px);
  transition: transform 0.3s ease;
}

.actor-card:hover .actor-image {
  transform: scale(1.1);
}

.actor-card:hover .image-overlay {
  opacity: 1;
}

.actor-card:hover .view-profile {
  transform: translateY(0);
}

.actor-info {
  text-align: center;
}

.actor-name {
  color: white;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.character-name {
  color: #a78bfa;
  font-size: 0.875rem;
}

@media (max-width: 1200px) {
  .actors-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 768px) {
  .actors-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 640px) {
  .actors-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .section-title {
    font-size: 1.5rem;
  }
}
</style>