<template>
  <div class="worldcup-page">
    <NavBar />
    <div class="content-container" v-if="!gameStarted">
      <div class="category-selection">
        <h1 class="worldcup-title">배우 이상형 월드컵</h1>
        <div class="category-buttons">
          <button 
            v-for="category in categories" 
            :key="category.value"
            @click="startGame(category.value)"
            class="category-button"
          >
            {{ category.label }}
          </button>
        </div>
      </div>
    </div>
    <WorldcupGame 
      v-else 
      :category="selectedCategory"
      @finish-game="gameStarted = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavBar from '@/components/common/NavBar.vue'
import WorldcupGame from '@/components/worldcup/WorldcupGame.vue'

const gameStarted = ref(false)
const selectedCategory = ref(null)

const categories = [
  { value: 9, label: '전체 배우' },
  { value: 2, label: '남자 배우' },
  { value: 1, label: '여자 배우' }
]

const startGame = (category) => {
  selectedCategory.value = category
  gameStarted.value = true
}
</script>

<style scoped>
.worldcup-page {
  background-color: #0b001a;
  min-height: 100vh;
  color: white;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 60px);
}

.category-selection {
  text-align: center;
  animation: fadeIn 0.8s ease-out;
}

.worldcup-title {
  font-size: 3.5rem;
  margin-bottom: 3rem;
  font-weight: 700;
  background: linear-gradient(45deg, #ffffff 30%, #8346ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 30px rgba(131, 70, 255, 0.3);
  letter-spacing: -1px;
  position: relative;
}

.worldcup-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: linear-gradient(to right, transparent, #8346ff, transparent);
}

.category-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
}

.category-button {
  padding: 1.2rem 2.5rem;
  font-size: 1.2rem;
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 30px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.category-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    45deg,
    rgba(131, 70, 255, 0) 0%,
    rgba(131, 70, 255, 0.1) 50%,
    rgba(131, 70, 255, 0) 100%
  );
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.category-button:hover {
  background: rgba(131, 70, 255, 0.2);
  border-color: #8346ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(131, 70, 255, 0.2);
}

.category-button:hover::before {
  transform: translateX(100%);
}

.category-button:active {
  transform: translateY(0);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .content-container {
    padding: 1.5rem;
  }

  .worldcup-title {
    font-size: 2.5rem;
    margin-bottom: 2rem;
  }

  .worldcup-title::after {
    width: 80px;
    bottom: -8px;
  }

  .category-buttons {
    flex-direction: column;
    gap: 1rem;
    padding: 0 1rem;
  }

  .category-button {
    padding: 1rem 2rem;
    width: 100%;
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .content-container {
    padding: 1rem;
  }

  .worldcup-title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }

  .category-button {
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
  }
}
</style>