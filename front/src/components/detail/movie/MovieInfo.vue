<template>
  <div class="info-section">
    <h1 class="movie-title animate-slide-up">{{ title }}</h1>
    <div class="action-icons animate-slide-up">
      <button 
        @click="$emit('wish')"
        :class="['icon-btn wish-btn', { 'wished': isWished }]"
        :title="isWished ? '찜 해제' : '찜하기'"
      >
        <span class="wish-icon">{{ isWished ? '❤️' : '🤍' }}</span>
      </button>
      <button 
        class="icon-btn" 
        @click="$emit('discuss')"
      >
        <span class="action-icon">💬</span>
      </button>
    </div>

    <div class="summary animate-slide-up">
      <h3 class="summary-title">줄거리</h3>
      <expandable-text 
        :text="overview" 
        :max-length="200"
        class="summary-text"
      />
    </div>

    <div class="action-buttons animate-slide-up">
      <button class="action-btn hover-effect">
        개봉년도: {{ formatYear(releaseDate) }}년
      </button>
      <button class="action-btn hover-effect">
        상영시간: {{ formatRuntime(runtime) }}
      </button>
      <button class="action-btn hover-effect">
        평점: {{ voteAverage.toFixed(1) }}점
      </button>
    </div>

    <div v-if="providers?.length" class="ott-section animate-slide-up">
      <h3 class="ott-title">OTT</h3>
      <div class="ott-platforms">
        <div v-for="provider in providers" 
             :key="provider.name" 
             class="ott-platform hover-effect">
          <img :src="provider.logo_path" :alt="provider.name" class="ott-logo" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ExpandableText from '@/components/detail/ExpandableText.vue';

defineProps({
  title: String,
  overview: String,
  releaseDate: String,
  runtime: Number,
  voteAverage: Number,
  providers: Array,
  isWished: {
    type: Boolean,
    default: false
  }
})

defineEmits(['wish', 'discuss'])

// 개봉년도 포맷
const formatYear = (date) => {
  return new Date(date).getFullYear()
}

// 러닝타임 포맷 (시간 분 형식)
const formatRuntime = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  if (hours > 0) {
    return `${hours}시간 ${remainingMinutes}분`
  }
  return `${minutes}분`
}
</script>

<style scoped>
.info-section {
  flex-grow: 1;
}

.movie-title {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
  background: linear-gradient(45deg, #ffffff, #8346ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: left;
}

.action-icons {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 50%;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.icon-btn:hover {
  background: rgba(131, 70, 255, 0.2);
  transform: scale(1.1);
}

.summary-title {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.summary-text {
  color: #c8c8c8;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.action-btn {
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid #8346ff;
  color: white;
  padding: 0.75rem 2rem;  /* 패딩 증가 */
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  white-space: nowrap;  /* 텍스트 줄바꿈 방지 */
  min-width: 180px;    /* 최소 너비 설정 */
  text-align: center;   /* 텍스트 중앙 정렬 */
  display: inline-flex; /* 인라인 플렉스로 변경 */
  align-items: center;  /* 세로 중앙 정렬 */
  justify-content: center; /* 가로 중앙 정렬 */
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  justify-content: flex-start; /* 왼쪽 정렬 */
}

.ott-section {
  margin-top: 2rem;
}

.ott-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.ott-platforms {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.ott-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.ott-platform:hover .ott-logo {
  transform: scale(1.1);
}

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 50%;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.icon-btn:hover {
  background: rgba(131, 70, 255, 0.2);
  transform: scale(1.1);
}

/* wished 상태일 때만 다르게 */
.icon-btn.wished {
  background: rgba(131, 70, 255, 0.3);
  border-color: #8346ff;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.wish-btn.wished .wish-icon {
  animation: heartBeat 0.3s ease-in-out;
}

@media (max-width: 768px) {
  .movie-title {
    font-size: 2rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 0.5rem;
  }

  .action-btn {
    width: 100%;
  }

  .ott-platforms {
    justify-content: center;
  }
}
@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
    gap: 0.8rem;
    width: 100%;
  }

  .action-btn {
    width: 100%;
    min-width: unset; /* 모바일에서는 최소 너비 제거 */
    padding: 0.75rem 1rem; /* 모바일에서 패딩 조정 */
  }
}
</style>