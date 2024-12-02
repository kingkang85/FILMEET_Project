<template>
  <div class="profile-card">
    <div class="profile-content">
      <div class="image-container">
        <img 
          :src="image" 
          :alt="name"
          class="profile-image"
        />
        <div class="image-overlay"></div>
      </div>
      
      <div class="info-container">
        <h1 class="profile-name">{{ name }}</h1>
        
        <div class="info-list">
          <div class="info-item">
            <span class="info-label">직업</span>
            <span>{{ role }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">생년월일</span>
            <span>{{ birthDate }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">출생</span>
            <span>{{ birthplace || '정보 없음' }}</span>
          </div>
        </div>

        <slot name="actions"></slot>

        <div v-if="biography" class="biography">
          <h3 class="biography-title">약력</h3>
          <expandable-text 
            :text="biography" 
            :max-length="300"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ExpandableText from '@/components/detail/ExpandableText.vue';
defineProps({
  image: String,
  name: String,
  role: String,
  birthDate: String,
  birthplace: String,
  biography: String,
})
</script>

<style scoped>
.profile-card {
  background: linear-gradient(
    to right,
    transparent,
    rgba(131, 70, 255, 0.05),
    transparent
  );
  border-radius: 12px;
  padding: 2rem;
  transition: transform 0.3s ease;
}

.profile-card:hover {
  transform: scale(1.02);
}

.profile-content {
  display: flex;
  gap: 2rem;
}

.image-container {
  width: 300px;
  flex-shrink: 0;
  position: relative;
}

.profile-image {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.image-container:hover .profile-image {
  box-shadow: 0 4px 25px rgba(131, 70, 255, 0.3);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.6), transparent);
  border-radius: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-container:hover .image-overlay {
  opacity: 1;
}

.info-container {
  flex: 1;
}

.profile-name {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  background: linear-gradient(to right, #a78bfa, #ec4899);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-label {
  color: #a78bfa;
  font-weight: 500;
  width: 100px;
}

.biography {
  margin-top: 2rem;
}

.biography-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #a78bfa;
  margin-bottom: 1rem;
}

.biography-text {
  color: #d1d1d1;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .profile-content {
    flex-direction: column;
  }

  .image-container {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
  }
}
</style>