<template>
  <div class="recommendation-section">
    <div class="recommendation-header">
      <img 
        :src="recommendedPlatformInfo.logo_path" 
        :alt="recommendedPlatformInfo.name"
        class="platform-logo"
      />
      <h2 class="recommendation-title">
        {{ movieStore.recommendedPlatform }}를 구독하는게 좋겠군요!
      </h2>
    </div>
    
    <div class="recommendation-details">
      <p>찜한 영화 {{ recommendedMovieCount }}개의 콘텐츠를 볼 수 있어요.</p>
      <p>월 {{ recommendedPlatformInfo.price.toLocaleString() }}원 ~</p>
    </div>

    <div class="action-buttons">
      <RouterLink :to="{ name: 'movielist' }" class="browse-button">
        더 알아보기
      </RouterLink>
      <a 
        :href="getSubscriptionUrl(movieStore.recommendedPlatform)" 
        target="_blank" 
        rel="noopener noreferrer"
        class="subscribe-button"
      >
        구독하러 가기
      </a>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { RouterLink } from 'vue-router'

const movieStore = useMovieStore()
// 추천된 플랫폼의 상세 정보 가져오기
const recommendedPlatformInfo = computed(() => {
  return movieStore.platforms.find(
    platform => platform.name === movieStore.recommendedPlatform
  )
})

// 추천된 플랫폼의 찜한 영화 수 계산
const recommendedMovieCount = computed(() => {
  const platformId = recommendedPlatformInfo.value?.id
  return platformId ? movieStore.moviesByPlatform[platformId]?.length || 0 : 0
})

// 구독 페이지 URL 반환
const getSubscriptionUrl = (platformName) => {
  const subscriptionUrls = {
    'NETFLIX': 'https://www.netflix.com/kr/',
    'WAVVE': 'https://www.wavve.com/index.html',
    'DISNEY PLUS': 'https://www.disneyplus.com/ko-kr',
    'WATCHA': 'https://watcha.com/browse/theater'
  }
  return subscriptionUrls[platformName] || '#'
}
</script>

<style scoped>
.recommendation-section {
  text-align: center;
  padding: 2.5rem 2rem;
  background: rgba(131, 70, 255, 0.05);
  border-radius: 16px;
  margin-top: 2rem;
  border: 1px solid rgba(131, 70, 255, 0.3);
}

.recommendation-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.platform-logo {
  height: 32px;
  width: auto;
  object-fit: contain;
}

.recommendation-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0;
  color: white;
  letter-spacing: 0.5px;
}

.recommendation-details {
  margin: 1.5rem 0;
  font-size: 1rem;
  color: #f8f8f8;
  opacity: 0.9;
}

.recommendation-details p {
  margin: 0.5rem 0;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.browse-button,
.subscribe-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 1.5rem;
  height: 44px;
  min-width: 140px;
  background: rgba(131, 70, 255, 0.8);
  color: white;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
}

.browse-button:hover,
.subscribe-button:hover {
  background: rgba(131, 70, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(131, 70, 255, 0.3);
}

@media (max-width: 768px) {
  .recommendation-section {
    padding: 2rem 1.5rem;
  }
  
  .recommendation-header {
    flex-direction: row;
  }
  
  .action-buttons {
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .browse-button,
  .subscribe-button {
    flex: 1;
    min-width: 120px;
  }
}
</style>