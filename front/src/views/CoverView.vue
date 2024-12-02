<script setup>
import { RouterLink } from 'vue-router';
import { onMounted, ref } from 'vue';

const showContent = ref(false);
const curtainOpen = ref(false);

onMounted(() => {
  // 커튼 먼저 열리고
  setTimeout(() => {
    curtainOpen.value = true;
  }, 500);

  // 그 다음 콘텐츠 표시
  setTimeout(() => {
    showContent.value = true;
  }, 2000);
});
</script>
<template>
  <main class="coverpage">
    <!-- 영사기 빔 효과 -->
    <div class="projector-beam"></div>
    <div class="projector-beam beam-second"></div>

    <!-- 필름 스트립 효과 -->
    <div class="film-strip left"></div>
    <div class="film-strip right"></div>

    <div class="content-wrapper" :class="{ 'show': showContent }">
      <div class="title-section">
        <div class="title-messages">
          <span class="glitch-text first-text">당신의 취향을 만나는 곳</span>
          <span class="glitch-text second-text">영화, 그리고 우리들의 이야기</span>
          <span class="glitch-text third-text">Find Your Cinema Life</span>
        </div>
        
        <div class="logo-wrapper">
          <svg class="logo" viewBox="0 0 500 100" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="neonGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#8346ff;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#a78bfa;stop-opacity:1" />
              </linearGradient>
              
              <filter id="softGlow">
                <feGaussianBlur stdDeviation="2" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            <!-- FILMEET 텍스트 -->
            <g class="logo-text" filter="url(#softGlow)">
              <!-- F -->
              <path d="M50 30 L50 80 M50 30 L90 30 M50 55 L80 55" />
              <!-- I -->
              <path d="M110 30 L110 80 M100 30 L120 30 M100 80 L120 80" />
              <!-- L -->
              <path d="M140 30 L140 80 L180 80" />
              <!-- M -->
              <path d="M200 80 L200 30 L225 70 L250 30 L250 80" />
              <!-- E -->
              <path d="M270 30 L270 80 M270 30 L310 30 M270 55 L300 55 M270 80 L310 80" />
              <!-- E -->
              <path d="M330 30 L330 80 M330 30 L370 30 M330 55 L360 55 M330 80 L370 80" />
              <!-- T -->
              <path d="M390 30 L450 30 M420 30 L420 80" />
            </g>
          </svg>
        </div>

        <div class="subtitle-messages">
          <span class="fade-text">새로운 영화의 발견</span>
          <span class="fade-text">당신만의 영화 컬렉션</span>
          <span class="fade-text">함께 나누는 영화 이야기</span>
        </div>

        <div class="button-wrapper">
          <RouterLink :to="{ name: 'main' }">
            <button class="start-btn">
              <span class="btn-text">START YOUR JOURNEY</span>
              <span class="btn-glow"></span>
            </button>
          </RouterLink>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
/* 기본 레이아웃 */
.coverpage {
  position: relative;
  width: 100vw;
  height: 100vh;
  background: #0B001A;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 영사기 빔 효과 */
.projector-beam {
  position: absolute;
  top: -50%;
  left: 50%;
  transform: translateX(-50%) rotate(45deg);
  width: 150px;
  height: 200vh;
  background: linear-gradient(
    to right,
    transparent,
    rgba(131, 70, 255, 0.05),
    rgba(131, 70, 255, 0.1),
    rgba(131, 70, 255, 0.05),
    transparent
  );
  animation: beam-move 8s ease-in-out infinite;
  opacity: 0.7;
}

.beam-second {
  animation-delay: -4s;
  width: 100px;
  opacity: 0.5;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  opacity: 0;
  transform: scale(0.95);
  transition: all 1s ease-out;
}

.content-wrapper.show {
  opacity: 1;
  transform: scale(1);
}

/* 타이틀 스타일링 */
.title-section {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.title-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.first-text {
  font-size: 2rem;
  font-weight: 300;
  color: #e5e5e5;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 2.5s;
}

.second-text {
  font-size: 2.5rem;
  font-weight: 500;
  color: #ffffff;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 3s;
  text-shadow: 0 0 10px rgba(131, 70, 255, 0.5);
}

.third-text {
  font-size: 1.8rem;
  font-weight: 300;
  color: #a78bfa;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 3.5s;
}

.subtitle-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  margin-top: 1rem;
}

.fade-text {
  font-size: 1.2rem;
  color: #e5e5e5;
  opacity: 0;
  animation: fadeIn 0.5s ease forwards;
}

.fade-text:nth-child(1) { animation-delay: 4s; }
.fade-text:nth-child(2) { animation-delay: 4.2s; }
.fade-text:nth-child(3) { animation-delay: 4.4s; }

/* 로고 스타일링 */
.logo-wrapper {
  margin: 3rem 0;
  width: 100%;
  display: flex;
  justify-content: center;
}

.logo {
  width: 90%;
  max-width: 700px;
  height: auto;
}

.logo-text path {
  fill: none;
  stroke: url(#neonGradient);
  stroke-width: 8;
  stroke-linecap: round;
  stroke-linejoin: round;
  animation: gentleGlow 3s ease-in-out infinite;
}

/* 시작 버튼 */
.button-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 3rem;
}

.start-btn {
  padding: 1.2rem 3.5rem;
  font-size: 1.4rem;
  background: linear-gradient(45deg, #8346ff, #4f9fff);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.start-btn:hover {
  transform: translateY(-3px);
  box-shadow: 
    0 5px 15px rgba(131, 70, 255, 0.3),
    0 0 30px rgba(131, 70, 255, 0.2);
}
.film-strip {
  position: absolute;
  top: 0;
  width: 30px;
  height: 100%;
  background-image: linear-gradient(
    to bottom,
    transparent 0%,
    transparent 40%,
    rgba(131, 70, 255, 0.2) 40%,
    rgba(131, 70, 255, 0.2) 60%,
    transparent 60%,
    transparent 100%
  );
  background-size: 100% 40px;
  animation: film-scroll 20s linear infinite;
  z-index: 1;
}

.film-strip.left { 
  left: 30px; 
}

.film-strip.right { 
  right: 30px; 
}

@keyframes film-scroll {
  0% { 
    background-position: 0 0; 
  }
  100% { 
    background-position: 0 100%; 
  }
}
/* 애니메이션 */
@keyframes beam-move {
  0%, 100% { transform: translateX(-70%) rotate(45deg); }
  50% { transform: translateX(-30%) rotate(45deg); }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 0.8;
    transform: translateY(0);
  }
}

@keyframes gentleGlow {
  0%, 100% {
    filter: drop-shadow(0 0 3px rgba(131, 70, 255, 0.5));
    opacity: 0.9;
  }
  50% {
    filter: drop-shadow(0 0 5px rgba(131, 70, 255, 0.7));
    opacity: 1;
  }
}

/* 반응형 */
@media (max-width: 768px) {
  .first-text {
    font-size: 1.5rem;
  }
  
  .second-text {
    font-size: 2rem;
  }

  .third-text {
    font-size: 1.5rem;
  }

  .fade-text {
    font-size: 1rem;
  }
  
  .logo {
    width: 95%;
  }
  
  .start-btn {
    padding: 1rem 2.5rem;
    font-size: 1.2rem;
  }
}
.film-strip {
    width: 20px;
  }
  
  .film-strip.left { 
    left: 10px; 
  }
  
  .film-strip.right { 
    right: 10px; 
  }
</style>