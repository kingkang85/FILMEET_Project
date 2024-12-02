<template>
  <div class="ai-recommend-modal" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3>AI 영화 추천</h3>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>
      
      <div class="chat-container" ref="chatContainer">
        <!-- 챗봇 메시지 -->
        <div v-for="message in messages" 
             :key="message.id" 
             :class="['message', message.type]"
        >
          <div class="message-content">{{ message.content }}</div>
          <div v-if="message.type === 'ai'" class="message-time">{{ message.time }}</div>
        </div>

        <!-- 추천 영화 카드 -->
        <div v-if="recommendedMovie" 
             :class="['movie-recommendation', `recommendation-${recommendedMovie.recommendation_type}`]"
        >
          <div class="recommendation-badge" v-if="recommendedMovie.recommendation_type">
            {{ getRecommendationTypeLabel(recommendedMovie.recommendation_type) }}
          </div>
          <div class="movie-card">
            <div class="movie-poster">
              <img 
                :src="recommendedMovie.poster_path" 
                :alt="recommendedMovie.title"
                @error="handleImageError"
              >
              <div class="movie-rating">
                <span class="star">★</span>
                {{ recommendedMovie.vote_average.toFixed(1) }}
              </div>
            </div>
            <div class="movie-info">
              <h4>{{ recommendedMovie.title }}</h4>
              <p class="overview">{{ recommendedMovie.overview }}</p>
              <div class="movie-meta">
                <div class="meta-item">
                  <span class="meta-label">개봉</span>
                  <span>{{ formatDate(recommendedMovie.release_date) }}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">장르</span>
                  <span>{{ formatGenres(recommendedMovie.genres) }}</span>
                </div>
                <div v-if="recommendedMovie.runtime" class="meta-item">
                  <span class="meta-label">상영시간</span>
                  <span>{{ formatRuntime(recommendedMovie.runtime) }}</span>
                </div>
              </div>
              <div class="action-buttons">
                <button 
                  class="detail-btn primary" 
                  @click="goToMovie(recommendedMovie.movie_id)"
                >
                  상세 정보
                </button>
                <button 
                  class="wishlist-btn"
                  :class="{ 'in-wishlist': isInWishlist }"
                  @click="toggleWishlist"
                >
                  <span class="icon">{{ isInWishlist ? '★' : '☆' }}</span>
                  {{ isInWishlist ? '찜됨' : '찜하기' }}
                </button>
              </div>
            </div>
          </div>
          <div v-if="recommendedMovie.note" class="recommendation-note">
            {{ recommendedMovie.note }}
          </div>
        </div>

        <!-- 로딩 표시 -->
        <div v-if="isLoading" class="loading-indicator">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
      <!-- 입력 섹션 -->
      <div class="input-section" :class="{ 'collapsed': isInputCollapsed }">
        <div class="input-toggle" @click="toggleInput">
          <span class="toggle-icon">{{ isInputCollapsed ? '↑' : '↓' }}</span>
          <span class="toggle-text">{{ isInputCollapsed ? '채팅 열기' : '채팅 닫기' }}</span>
        </div>
      <!-- 찜 제외하기 -->
      <div class="recommendation-settings" :class="{ 'highlight': highlightExcludeOption }">
        <label class="setting-option">
          <input 
            type="checkbox" 
            v-model="excludeWishlisted"
          >
          <span>찜한 영화 제외하기</span>
        </label>
      </div>

        <div class="input-container" :class="{ 'hidden': isInputCollapsed }">
          <div class="input-wrapper">
            <textarea 
              v-model="userInput"
              placeholder="어떤 영화를 찾고 계신가요? (예: 액션 영화 추천해줘, 로맨스 코미디 찾아줘)"
              @keyup.enter.exact.prevent="sendMessage"
              @keyup.enter.shift.exact.prevent="userInput += '\n'"
              :disabled="isLoading"
              ref="inputField"
            ></textarea>
            <button 
              :disabled="isLoading || !userInput.trim()"
              @click="sendMessage"
              class="send-btn"
            >
              <span v-if="isLoading">추천 중...</span>
              <span v-else>추천 받기</span>
            </button>
          </div>
          <div class="suggestion-chips" v-if="!userInput.trim()">
            <button 
              v-for="suggestion in suggestions" 
              :key="suggestion"
              class="chip"
              @click="applySuggestion(suggestion)"
            >
              {{ suggestion }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import { useUserStore } from '@/stores/user'
import { useAIRecommendationStore } from '@/stores/aiRecommendation'
import { format } from 'date-fns'
import { ko } from 'date-fns/locale'
import ChatMessage from './ChatMessage.vue'
import MovieCard from './MovieCard.vue'
import { useWishStore } from '@/stores/wishlist'

const props = defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close'])
const router = useRouter()
const movieStore = useMovieStore()
const userStore = useUserStore()
const wishStore = useWishStore()
const aiStore = useAIRecommendationStore()

// 상태 관리
const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const recommendedMovie = ref(null)
const chatContainer = ref(null)
const inputField = ref(null)
const isInWishlist = ref(false)
const excludeWishlisted = computed({
  get: () => aiStore.excludeWishlisted,
  set: (value) => aiStore.setExcludeWishlisted(value)
})

// 추천 제안
const suggestions = [
  '재미있는 액션 영화 추천해줘',
  '감동적인 드라마 찾아줘',
  '로맨스 코미디 보고싶어',
  '최근에 개봉한 SF 영화 추천해줘',
  '평점 높은 애니메이션 알려줘'
]

// 유틸리티 함수들
const formatDate = (date) => {
  try {
    return format(new Date(date), 'yyyy년 M월 d일', { locale: ko })
  } catch {
    return '날짜 정보 없음'
  }
}

const formatRuntime = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  return `${hours}시간 ${remainingMinutes}분`
}

const formatGenres = (genres) => {
  return genres?.map(g => g.name).join(', ') || '장르 정보 없음'
}

const getRecommendationTypeLabel = (type) => {
  const labels = {
    'ai': 'AI 추천',
    'personalized': '맞춤 추천',
    'keyword': '키워드 추천'
  }
  return labels[type] || ''
}

const handleImageError = (event) => {
  event.target.src = '/default-movie-poster.png'
}

// 메시지 관리
const addMessage = (content, type = 'user') => {
  messages.value.push({
    id: Date.now(),
    content,
    type,
    time: format(new Date(), 'HH:mm')
  })
  scrollToBottom()
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 위시리스트 관리 부분 수정
const toggleWishlist = async () => {
  if (!recommendedMovie.value) return
  
  try {
    await wishStore.toggleMovieWish(recommendedMovie.value.movie_id)
    isInWishlist.value = wishStore.isMovieInWishlist(recommendedMovie.value.movie_id)
  } catch (error) {
    addMessage('위시리스트 업데이트 중 오류가 발생했습니다.', 'system')
  }
}



const checkWishlistStatus = () => {
  if (!recommendedMovie.value) return
  isInWishlist.value = wishStore.isMovieInWishlist(recommendedMovie.value.movie_id)
}

// 네비게이션
const goToMovie = (movieId) => {
  router.push({ name: 'moviedetail', params: { id: movieId } })
  emit('close')
}

// 제안 적용
const applySuggestion = (suggestion) => {
  userInput.value = suggestion
  inputField.value?.focus()
}

// 라이프사이클 훅
onMounted(async () => {
  addMessage('안녕하세요! 어떤 영화를 찾고 계신가요?', 'ai')
  inputField.value?.focus()
  
  // 위시리스트 초기 로드
  try {
    await wishStore.getMovieWishlist()
  } catch (error) {
    console.error('위시리스트 로드 실패:', error)
  }
})

// 창이 열릴 때마다 포커스
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    nextTick(() => {
      inputField.value?.focus()
    })
  }
})
const handleClose = () => {
  if (!isLoading.value) {
    emit('close')
  }
}

// 입력 영역 상태 관리
const isInputCollapsed = ref(false)

// 입력 영역 토글 함수
const toggleInput = () => {
  isInputCollapsed.value = !isInputCollapsed.value
}

// AIRecommendation.vue의 sendMessage 함수 수정
const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return
  
  const input = userInput.value
  userInput.value = ''
  addMessage(input)
  isLoading.value = true
  recommendedMovie.value = null

  try {
    // 위시리스트에 있는 영화 ID 목록 가져오기
    const wishedMovieIds = wishStore.movieWishlist.map(m => m.movie_id)
    
    // 추천 요청
    const result = await aiStore.getRecommendation(input, {
      excludeMovieIds: wishedMovieIds
    })

    // ALL_MOVIES_WISHLISTED 에러 처리
    if (result && result.code === 'ALL_MOVIES_WISHLISTED') {
      addMessage('현재 모든 영화가 찜 목록에 있습니다.', 'system')
      addMessage('찜한 영화 제외 옵션을 해제하고 다시 시도해보세요.', 'system')
      
      // 찜한 영화 제외 옵션 강조
      highlightExcludeOption.value = true

      // 찜 제외 옵션 자동 해제 (선택사항)
      // excludeWishlisted.value = false
      
      return
    }

    // 정상적인 추천 결과 처리
    if (result && result.movie) {
      recommendedMovie.value = result.movie
      addMessage(result.message, 'ai')
      
      if (result.note) {
        addMessage(result.note, 'system')
      }
      
      await checkWishlistStatus()
      isInputCollapsed.value = true
    }

  } catch (error) {
    console.error('추천 에러:', error)
    let errorMessage = '죄송합니다. 영화 추천 중 오류가 발생했습니다.'
    
    // 특정 에러 케이스 처리
    if (error.response?.data?.code === 'ALL_MOVIES_WISHLISTED') {
      errorMessage = '현재 모든 영화가 찜 목록에 있습니다. 찜한 영화 제외 옵션을 해제하고 다시 시도해보세요.'
      highlightExcludeOption.value = true
    }
    
    addMessage(errorMessage, 'system')
  } finally {
    isLoading.value = false
  }
}

// 옵션 강조 표시를 위한 상태 추가
const highlightExcludeOption = ref(false);

// 옵션 변경 시 강조 표시 제거
watch(excludeWishlisted, () => {
  highlightExcludeOption.value = false;
});
</script>


<style scoped>
/* Base Modal */
.ai-recommend-modal {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
}

.modal-content {
  width: 90%;
  max-width: 600px;
  height: 80vh;
  display: flex;
  flex-direction: column;
  border-radius: 1rem;
  background: #1a1a2e;
  border: 1px solid rgba(131, 70, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-radius: 1rem 1rem 0 0;
  background: rgba(131, 70, 255, 0.05);
  border-bottom: 1px solid rgba(131, 70, 255, 0.2);
  position: relative;
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
}

.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.8rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: rotate(90deg);
}

/* Chat Container */
.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

.chat-container::-webkit-scrollbar-thumb {
  background: rgba(131, 70, 255, 0.3);
  border-radius: 3px;
}

/* Messages */
.message {
  max-width: 80%;
  padding: 1rem;
  border-radius: 0.75rem;
  line-height: 1.5;
  animation: messageSlide 0.3s ease;
}

.message.user {
  margin-left: auto;
  background: rgba(131, 70, 255, 0.2);
  color: white;
}

.message.ai {
  margin-right: auto;
  background: rgba(255, 255, 255, 0.05);
  color: #e5e5e5;
}

.message.system {
  margin: 0 auto;
  max-width: 90%;
  background: rgba(255, 193, 7, 0.1);
  color: #ffe082;
  font-size: 0.875rem;
  font-style: italic;
  text-align: center;
  padding: 0.5rem;
}

/* Movie Card */
.movie-recommendation {
  width: 100%;
  margin: 1rem 0;
  position: relative;
}

.recommendation-badge {
  position: absolute;
  top: -0.75rem;
  right: 1rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  z-index: 10;
  background: #8346ff;
  color: white;
  box-shadow: 0 2px 4px rgba(131, 70, 255, 0.3);
}

.movie-card {
  overflow: hidden;
  border-radius: 0.75rem;
  transition: transform 0.3s ease;
  background: rgba(255, 255, 255, 0.05);
}

.movie-card:hover {
  transform: translateY(-2px);
}

/* Movie Poster */
.movie-poster {
  position: relative;
}

.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-rating {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
}

.star {
  color: #ffd700;
}

.message-time {
  font-size: 0.9rem;
  color:#888
}

/* Movie Info */
.movie-info {
  padding: 1rem;
  display: grid;
  gap: 1rem;
}

.movie-info h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
}

.overview {
  color: #d1d1d1;
  font-size: 0.875rem;
  line-height: 1.6;
  margin: 1rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: keep-all;
}

/* Meta Information */
.movie-meta {
  display: grid;
  gap: 0.5rem;
}

.meta-item {
  display: grid;
  grid-template-columns: 5rem 1fr;
  align-items: center;
  font-size: 0.875rem;
  color: #d1d1d1;
  line-height: 1.5;
}

.meta-label {
  color: #888;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.detail-btn,
.wishlist-btn {
  flex: 1;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detail-btn {
  background: #8346ff;
  color: white;
  border: none;
}

.detail-btn:hover {
  background: #9666ff;
}

.wishlist-btn {
  background: transparent;
  border: 1px solid rgba(131, 70, 255, 0.3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
}

.wishlist-btn:hover {
  background: rgba(131, 70, 255, 0.1);
}

.wishlist-btn.in-wishlist {
  background: rgba(255, 215, 0, 0.1);
  border-color: #ffd700;
  color: #ffd700;
}

/* Input Area */
.input-container {
  padding: 1.25rem;
  border-top: 1px solid rgba(131, 70, 255, 0.2);
  background: rgba(131, 70, 255, 0.02);
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

textarea {
  width: 100%;
  height: 5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 0.5rem;
  color: white;
  resize: none;
  font-size: 0.875rem;
  line-height: 1.5;
}

textarea:focus {
  outline: none;
  border-color: #8346ff;
  box-shadow: 0 0 0 2px rgba(131, 70, 255, 0.2);
}

.send-btn {
  width: 100%;
  padding: 0.75rem;
  background: #8346ff;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-btn:not(:disabled):hover {
  background: #9666ff;
  transform: translateY(-2px);
}

.send-btn:disabled {
  background: #444;
  opacity: 0.7;
  cursor: not-allowed;
}

/* Suggestion Chips */
.suggestion-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.chip {
  padding: 0.5rem 1rem;
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 9999px;
  color: white;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chip:hover {
  background: rgba(131, 70, 255, 0.2);
  transform: translateY(-2px);
}

/* Loading Indicator */
.loading-indicator {
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
}

.typing-indicator span {
  width: 0.5rem;
  height: 0.5rem;
  background: #8346ff;
  border-radius: 50%;
  animation: bounce 0.5s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.1s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.2s;
}

/* Animations */
@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    height: 90vh;
  }
  
  .message {
    max-width: 90%;
  }
  
  .movie-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
}

.input-section {
  position: relative;
  transition: all 0.3s ease;
}

.input-toggle {
  position: absolute;
  top: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(131, 70, 255, 0.2);
  padding: 0.25rem 1rem;
  border-radius: 1rem 1rem 0 0;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.input-toggle:hover {
  background: rgba(131, 70, 255, 0.3);
}

.toggle-icon {
  transition: transform 0.3s ease;
}

.input-section.collapsed .input-container {
  height: 0;
  overflow: hidden;
  padding: 0;
  opacity: 0;
}

.input-section.collapsed .input-toggle {
  background: #8346ff;
}

.input-container {
  height: auto;
  opacity: 1;
  transition: all 0.3s ease;
}

/* 애니메이션 수정 */
.input-container.hidden {
  height: 0;
  overflow: hidden;
  padding: 0;
  opacity: 0;
}

/* 입력 영역이 접혔을 때 하단 여백 조정 */
.modal-content {
  padding-bottom: 2rem;
}

.recommendation-settings {
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid rgba(131, 70, 255, 0.2);
  background: rgba(131, 70, 255, 0.05);
}

.setting-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ddd;
  font-size: 0.875rem;
  cursor: pointer;
}

.setting-option input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
  accent-color: #8346ff;
  cursor: pointer;
}
.recommendation-settings.highlight {
  animation: pulse 2s infinite;
  border: 2px solid #8346ff;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(131, 70, 255, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(131, 70, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(131, 70, 255, 0);
  }
}
</style>