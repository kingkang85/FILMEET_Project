<template>
  <div id="app">
    <router-view></router-view>
    
    <!-- AI 추천 플로팅 버튼 -->
    <button 
      v-if="isLoggedIn" 
      class="ai-floating-btn"
      @click="showAIModal = true"
    >
      <span class="ai-icon">🎬</span>
      <span class="btn-text">AI 추천</span>
    </button>

    <!-- AI 추천 모달 -->
    <AIRecommendation
      v-if="showAIModal"
      :is-open="showAIModal"
      @close="showAIModal = false"
    />

    <!-- 엔딩 크레딧 -->
    <EndingCredits 
      v-if="userStore.showEndingCredits" 
      :show="userStore.showEndingCredits"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import AIRecommendation from '@/components/AIRecommendation.vue'
import EndingCredits from '@/components/EndingCredits.vue'

const userStore = useUserStore()
const showAIModal = ref(false)

const isLoggedIn = computed(() => !!userStore.user)
</script>

<style>
/* Floating Button */
.ai-floating-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 1.5rem;
  background-color: #9666ff;
  border: none;
  border-radius: 50px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  box-shadow: 0 4px 12px rgba(131, 70, 255, 0.3);
  transition: all 0.3s ease;
  z-index: 1000;
  font-size: 1rem;
  font-weight: 500;
}

.ai-floating-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(132, 70, 255, 0.623);
}

.ai-icon {
  font-size: 1.5rem;
}

.btn-text {
  white-space: nowrap;
}

/* 엔딩 크레딧이 모든 요소 위에 표시되도록 z-index 조정 */
.ending-credits {
  z-index: 9999;
}
@font-face {
    font-family: 'Danjo-bold-Regular';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2307-1@1.1/Danjo-bold-Regular.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
}
:root {
    font-family: 'Danjo-bold-Regular', sans-serif;
}

@media (max-width: 768px) {
  .ai-floating-btn {
    bottom: 1.5rem;
    right: 1.5rem;
    padding: 0.8rem 1.2rem;
  }
}
</style>