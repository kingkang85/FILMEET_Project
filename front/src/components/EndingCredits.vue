<template>
  <div class="ending-credits" v-if="show">
    <div class="credits-content" ref="creditsContent">
      <div class="thanks-section">
        <h1>감사합니다</h1>
        <p>지금까지 저희 서비스를 이용해주셔서 감사합니다</p>
      </div>

      <div class="project-section">
        <h2>🎬 MovieCurators</h2>
        <p>마지막까지 함께해 주셔서 감사합니다</p>
      </div>

      <div class="credit-section">
        <h3>🚀 Made with</h3>
        <div class="tech-list">
          <div class="tech-group">
            <h4>Frontend</h4>
            <p>Vue.js</p>
            <p>Pinia</p>
            <p>Vue Router</p>
            <p>Axios</p>
          </div>
          <div class="tech-group">
            <h4>Backend</h4>
            <p>Django</p>
            <p>DRF</p>
            <p>SQLite</p>
            <p>OpenAI</p>
          </div>
        </div>
      </div>

      <div class="feature-section">
        <h3>✨ Features</h3>
        <p>AI 기반 영화 추천 시스템</p>
        <p>배우 이상형 월드컵</p>
        <p>영화·배우·감독 위시리스트</p>
        <p>영화 토론의 장</p>
      </div>

      <div class="team-section">
        <h3>👥 Team</h3>
        <div class="member-list">
          <div class="member">강현호 - Fullstack</div>
          <div class="member">강지민 - Fullstack</div>
        </div>
      </div>

      <div class="ending-section">
        <h2>🌟 또 만나요!</h2>
        <p>더 나은 서비스로 돌아오겠습니다</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'  // userStore import 추가

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['update:show'])
const router = useRouter()
const userStore = useUserStore()  // userStore 사용
const creditsContent = ref(null)

const handleExit = () => {
  emit('update:show', false)
  // 토큰과 유저 정보 초기화
  userStore.user = null
  userStore.token = null
  // 강제로 페이지 새로고침 후 홈으로 이동
  window.location.href = '/'
}

onMounted(() => {
  if (props.show) {
    setTimeout(() => {
      emit('update:show', false)
      userStore.user = null
      userStore.token = null
      window.location.href = '/'
    }, 20000)
  }
})
</script>
<style scoped>
.ending-credits {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: #000;
  color: #fff;
  overflow: hidden;
  z-index: 9999;
}

/* 나가기 버튼 스타일 */
.exit-button {
  position: fixed;
  top: 2rem;
  right: 2rem;
  padding: 0.8rem 1.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 2rem;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  z-index: 10000;
  transition: all 0.3s ease;
}

.exit-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.credits-content {
  position: absolute;
  width: 100%;
  padding: 2rem;
  animation: scrollCredits 20s linear forwards;
}

.thanks-section {
  text-align: center;
  margin-bottom: 4rem;
}

.thanks-section h1 {
  font-size: 3rem;
  color: #FFD700;
  margin-bottom: 1rem;
}

.project-section {
  text-align: center;
  margin-bottom: 3rem;
}

.project-section h2 {
  font-size: 2.5rem;
  color: #FFD700;
  margin-bottom: 1rem;
}

.credit-section,
.feature-section,
.team-section {
  text-align: center;
  margin-bottom: 3rem;
}

h3 {
  font-size: 2rem;
  color: #FFD700;
  margin-bottom: 1.5rem;
}

.tech-list {
  display: flex;
  justify-content: center;
  gap: 4rem;
  margin: 1rem 0;
}

.tech-group h4 {
  color: #FFA500;
  margin-bottom: 1rem;
}

.tech-group p {
  margin: 0.5rem 0;
  font-size: 1.2rem;
}

.member-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.member {
  font-size: 1.2rem;
}

.ending-section {
  text-align: center;
  margin-top: 4rem;
}

.ending-section h2 {
  font-size: 2.5rem;
  color: #FFD700;
  margin-bottom: 1rem;
}

@keyframes scrollCredits {
  0% {
    transform: translateY(100vh);
  }
  100% {
    transform: translateY(-100%);
  }
}
</style>