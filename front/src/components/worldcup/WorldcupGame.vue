<template>
  <div class="game-container">
    <template v-if="!gameCompleted">
      <div class="game-info">
        <h2>{{ currentRoundText }}</h2>
        <p>{{ currentMatch + 1 }}/{{ totalMatches }} 경기</p>
      </div>
  
      <div class="match-container" v-if="currentMatchData">
        <div 
          v-for="actor in [currentMatchData.actor1, currentMatchData.actor2]"
          :key="actor.id"
          @click="selectWinner(actor)"
          class="actor-card"
        >
          <div class="actor-image">
            <img :src="actor.profile_path" :alt="actor.name">
          </div>
          <div class="actor-name">{{ actor.name }}</div>
        </div>
      </div>
    </template>

    <WorldcupResult 
      v-if="gameCompleted"
      :winner="winner"
      @restart="$emit('finish-game')"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import WorldcupResult from '@/components/worldcup/WorldcupResult.vue'
import axios from 'axios'

const props = defineProps({
  category: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['finish-game'])

const gameId = ref(null)
const matches = ref([])
const currentMatch = ref(0)
const currentRound = ref(5)
const winner = ref(null)
const gameCompleted = ref(false)

const currentMatchData = computed(() => {
  if (!matches.value.length) return null
  return matches.value[currentMatch.value]
})

const currentRoundText = computed(() => {
  const roundMap = {
    5: '32강',
    4: '16강',
    3: '8강',
    2: '4강',
    1: '결승'
  }
  return roundMap[currentRound.value]
})

const totalMatches = computed(() => 
  matches.value.length
)

const startGame = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/v1/worldcup/start/', {
      category: props.category
    })
    gameId.value = response.data.game_id
    matches.value = response.data.matches
  } catch (error) {
    console.error('게임 시작 실패:', error)
  }
}

const selectWinner = async (actor) => {
  console.log("Current Match Data:", currentMatchData.value)
  console.log("Winner Actor:", actor)
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/v1/worldcup/submit_match/', {
      match_id: currentMatchData.value.match_id,
      winner_id: actor.person_id,
      round: currentRound.value
    })
    if (response.data.game_completed) {
      winner.value = response.data.winner
      gameCompleted.value = true
    } else if (response.data.next_round) {
      matches.value = response.data.matches
      currentMatch.value = 0
      currentRound.value--
    } else {
      currentMatch.value++
    }
  } catch (error) {
    console.error('승자 선택 실패:', error)
  }
}

onMounted(startGame)
</script>

<style scoped>
.game-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.game-info {
  text-align: center;
  margin-bottom: 2rem;
}

.game-info h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.match-container {
  display: flex;
  gap: 2rem;
  justify-content: center;
}

.actor-card {
  flex: 1;
  max-width: 400px;
  cursor: pointer;
  transition: transform 0.3s;
  border-radius: 12px;
  overflow: hidden;
  background-color: #2c0052;
}

.actor-card:hover {
  transform: scale(1.02);
}

.actor-image {
  position: relative;
  padding-top: 150%;
}

.actor-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.actor-name {
  padding: 1rem;
  text-align: center;
  font-size: 1.2rem;
  background-color: rgba(0, 0, 0, 0.5);
}

@media (max-width: 768px) {
  .match-container {
    flex-direction: column;
    gap: 1rem;
  }

  .actor-card {
    max-width: none;
  }
}
</style>