<!-- ExploreView.vue -->
<template>
  <div class="search-page">
    <NavBar />
    
    <div class="content-container">
      <!-- Search Section -->
      <div class="search-section">
        <div class="search-container">
          <div class="search-input-wrapper">
            <input 
              type="text"
              class="search-input"
              placeholder="영화를 검색해 보세요"
              v-model="searchQuery"
              @input="handleSearch"
              @keyup.enter="performSearch"
            />
            <!-- Recent Searches Dropdown -->
            <div v-if="showRecentSearches && recentSearches.length" class="recent-searches">
              <div class="recent-searches-header">
                <span>최근 검색어</span>
                <button @click="clearRecentSearches" class="clear-searches">전체 삭제</button>
              </div>
              <div 
                v-for="(search, index) in recentSearches" 
                :key="index" 
                class="recent-search-item"
                @click="useRecentSearch(search)"
              >
                <span>{{ search }}</span>
                <button @click.stop="removeRecentSearch(index)" class="remove-search">×</button>
              </div>
            </div>
          </div>
          <button class="search-button" @click="performSearch">
            검색
          </button>
        </div>

        <!-- Filter Tags -->
        <div class="filter-tags">
          <button 
            v-for="tag in filterTags" 
            :key="tag.id"
            :class="['filter-tag', { active: tag.active }]"
            @click="setActiveFilter(tag)"
          >
            {{ tag.name }}
          </button>
        </div>

        <!-- Genre Filter -->
        <div v-if="showGenreFilter" class="genre-filter">
          <button 
            v-for="genre in genreList" 
            :key="genre.id"
            :class="['genre-btn', { active: selectedGenreId === genre.id }]"
            @click="toggleGenre(genre.id)"
          >
            {{ genre.name }}
          </button>
        </div>

        <!-- Search Results -->
        <TransitionGroup 
          name="fade" 
          tag="div" 
          class="search-results" 
          v-if="showResults || isLoading"
        >
          <h2 key="title" class="results-title" v-if="!isLoading">
            "{{ searchQuery }}" 검색 결과 ({{ filteredMovies.length }}개)
          </h2>

          <!-- Loading State -->
          <div key="loading" v-if="isLoading" class="results-grid">
            <MovieSkeleton v-for="n in 10" :key="`skeleton-${n}`" />
          </div>

          <!-- Results Grid -->
          <div 
            key="results" 
            v-else-if="filteredMovies.length" 
            class="results-grid"
            ref="resultsContainer"
          >
            <div 
              v-for="(movie, index) in displayedMovies" 
              :key="movie.id" 
              class="movie-card"
              :style="{ animationDelay: `${index * 0.05}s` }"
            >
              <div class="poster-wrapper">
                <img 
                  :src="movie.poster_path" 
                  :alt="movie.title" 
                  class="movie-poster"
                  loading="lazy"
                />
                <div class="movie-overlay">
                  <div class="movie-actions">
                    <button 
                      @click.stop="toggleWishMovie(movie.movie_id)"
                      :class="['action-btn wish-btn', { 'wished': isMovieWished(movie.movie_id) }]"
                      :title="isMovieWished(movie.movie_id) ? '찜 해제' : '찜하기'"
                    >
                      <span class="wish-icon">
                        {{ isMovieWished(movie.movie_id) ? '❤️' : '🤍' }}
                      </span>
                    </button>
                  </div>
                  <router-link :to="{ name: 'moviedetail', params: { id: movie.movie_id }}">
                    <button class="detail-btn">상세정보 보기</button>
                  </router-link>
                </div>
              </div>
              <h3 class="movie-title">{{ movie.title }}</h3>
            </div>
          </div>

          <!-- Loading More Indicator -->
          <div v-if="isLoadingMore" key="loading-more" class="loading-more">
            더 많은 영화를 불러오는 중... 🎬
          </div>

          <!-- No Results -->
          <div key="no-results" v-if="!isLoading && filteredMovies.length === 0" class="no-results">
            검색 결과가 없습니다 😢
          </div>
        </TransitionGroup>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import NavBar from '@/components/common/NavBar.vue';
import MovieSkeleton from '@/components/MovieSkeleton.vue';
import { useMovieStore } from '@/stores/movie';
import { useRouter } from 'vue-router';
import { useWishStore } from '@/stores/wishlist'
import { useUserStore } from '@/stores/user'
import axios from 'axios';

const route = useRouter()
const movieStore = useMovieStore();
const searchQuery = ref('');
const showResults = ref(false);
const isLoading = ref(false);
const isLoadingMore = ref(false);
const activeFilter = ref('latest');
const selectedGenreId = ref(null);
const currentPage = ref(1);
const itemsPerPage = 20;
const showRecentSearches = ref(false);
const resultsContainer = ref(null);
const wishStore = useWishStore()
const userStore = useUserStore()


// 최근 검색어 (localStorage 사용)
const recentSearches = ref(JSON.parse(localStorage.getItem('recentSearches') || '[]'));

// Genre List
const genreList = [
  { id: 28, name: '액션' },
  { id: 12, name: '어드벤처' },
  { id: 16, name: '애니메이션' },
  { id: 35, name: '코미디' },
  { id: 80, name: '범죄' },
  { id: 99, name: '다큐멘터리' },
  { id: 18, name: '드라마' },
  { id: 10751, name: '가족' },
  { id: 14, name: '판타지' },
  { id: 36, name: '역사' },
  { id: 27, name: '공포' },
  { id: 10402, name: '음악' },
  { id: 9648, name: '미스터리' },
  { id: 10749, name: '로맨스' },
  { id: 878, name: 'SF' },
  { id: 53, name: '스릴러' },
  { id: 10752, name: '전쟁' },
  { id: 37, name: '서부' }
];

const filterTags = ref([
  { id: 1, name: '최신순', value: 'latest', active: true },
  { id: 2, name: '인기순', value: 'popularity', active: false },
  { id: 3, name: '평점순', value: 'rating', active: false },
  { id: 4, name: '장르별', value: 'genre', active: false },
]);
const getHeaders = () => {
    const token = userStore.token
    if (!token) {
      throw new Error('Authentication token is missing')
    }
    return {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    }
  }
// 장르 필터 표시 여부
const showGenreFilter = computed(() => {
  return filterTags.value.find(tag => tag.value === 'genre')?.active;
});

// 필터링된 영화 목록
const filteredMovies = computed(() => {
  if (!searchQuery.value.trim() || !movieStore.movies) return [];
  
  let results = movieStore.movies.filter(movie => 
    movie.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    movie.original_title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
  
  // 장르 필터링
  if (selectedGenreId.value) {
    results = results.filter(movie => 
      movie.genres.some(genre => genre.genre_id === selectedGenreId.value)
    );
  }
  
  // 정렬
  switch (activeFilter.value) {
    case 'popularity':
      results.sort((a, b) => b.popularity - a.popularity);
      break;
    case 'rating':
      results.sort((a, b) => b.vote_average - a.vote_average);
      break;
    case 'latest':
    default:
      results.sort((a, b) => new Date(b.release_date) - new Date(a.release_date));
      break;
  }
  
  return results;
});

// 현재 페이지에 표시할 영화 목록
const displayedMovies = computed(() => {
  const endIndex = currentPage.value * itemsPerPage;
  return filteredMovies.value.slice(0, endIndex);
});

// 최근 검색어 관리
const addRecentSearch = (query) => {
  if (!query.trim()) return;
  
  const searches = recentSearches.value.filter(s => s !== query);
  searches.unshift(query);
  recentSearches.value = searches.slice(0, 5);
  localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value));
};

const removeRecentSearch = (index) => {
  recentSearches.value.splice(index, 1);
  localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value));
};

const clearRecentSearches = () => {
  recentSearches.value = [];
  localStorage.setItem('recentSearches', '[]');
};

const useRecentSearch = (query) => {
  searchQuery.value = query;
  showRecentSearches.value = false;
  performSearch();
};

// 무한 스크롤
const handleScroll = async () => {
  if (isLoadingMore.value) return;

  const container = resultsContainer.value;
  if (!container) return;

  const bottomOfWindow = window.scrollY + window.innerHeight >= container.offsetTop + container.offsetHeight - 200;

  if (bottomOfWindow && displayedMovies.value.length < filteredMovies.value.length) {
    isLoadingMore.value = true;
    await new Promise(resolve => setTimeout(resolve, 500)); // 로딩 시뮬레이션
    currentPage.value++;
    isLoadingMore.value = false;
  }
};

// 검색 핸들러 (디바운스)
let searchTimeout;
const handleSearch = () => {
  clearTimeout(searchTimeout);
  showRecentSearches.value = true;
  
  // 디바운스 시간을 100ms로 줄임
  searchTimeout = setTimeout(() => {
    if (searchQuery.value.trim()) {
      showResults.value = true;
      // 실시간 검색 결과를 보여주되, 검색 기록은 저장하지 않음
      if (!movieStore.movies.length) {
        movieStore.fetchMovies();
      }
    }
  }, 100); // 100ms
};

// 검색 실행
const performSearch = async () => {
  if (!searchQuery.value.trim()) return;
  
  isLoading.value = true;
  showResults.value = true;
  showRecentSearches.value = false;
  currentPage.value = 1;
  
  try {
    if (!movieStore.movies.length) {
      await movieStore.fetchMovies();
    }
    if (userStore.isLoggedIn) {  // 로그인된 경우에만
      await wishStore.getMovieWishlist(); // 위시리스트 갱신
    }
    addRecentSearch(searchQuery.value);
  } catch (error) {
    console.error('검색 중 오류 발생:', error);
  } finally {
    isLoading.value = false;
  }
};

// 필터 변경
const setActiveFilter = (tag) => {
  filterTags.value.forEach(t => t.active = t.id === tag.id);
  activeFilter.value = tag.value;
  currentPage.value = 1;
};

// 장르 토글
const toggleGenre = (genreId) => {
  selectedGenreId.value = selectedGenreId.value === genreId ? null : genreId;
  currentPage.value = 1;
};

// 라이프사이클 훅
onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  movieStore.fetchMovies();
  wishStore.getMovieWishlist();
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

// 영화 찜하기 상태 확인
const isMovieWished = (movieId) => {
  return wishStore.isMovieInWishlist(movieId)
}

// 찜하기 토글 함수
const toggleWishMovie = async (movieId) => {
  try {
    if (!userStore.isLoggedIn) {
      alert('로그인이 필요한 서비스입니다.')
      route.push('/login')
      return
    }

    await axios.post(
      `http://127.0.0.1:8000/api/v1/movies/${movieId}/wishlist/`,
      {}, // 빈 객체를 데이터로 전달
      getHeaders() // 헤더 설정을 마지막 인자로 전달
    )
    await wishStore.getMovieWishlist()
  } catch (err) {
    console.error('Error toggling movie wish:', err)
  }
}

</script>

<style scoped>
/* Base Layout */
.search-page {
  background-color: #0b001a;
  min-height: 100vh;
  color: white;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.search-section {
  margin-top: 2rem;
}

/* Search Components */
.search-container {
  display: flex;
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.search-input-wrapper {
  position: relative;
  flex-grow: 1;
}

.search-input {
  width: 100%;
  padding: 1.2rem 2rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid;
  border-image: linear-gradient(to right, #8346ff, #4f9fff) 1;
  color: white;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 20px rgba(131, 70, 255, 0.2);
}

.search-input::placeholder {
  color: #666;
}

.search-button {
  padding: 0 2.5rem;
  border-radius: 8px;
  border: none;
  background: linear-gradient(45deg, #8346ff, #4f9fff);
  color: white;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.search-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(131, 70, 255, 0.3);
}

.search-button::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: 0.5s;
}

.search-button:hover::after {
  left: 100%;
}

/* Recent Searches Dropdown */
.recent-searches {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #1a0033;
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 8px;
  margin-top: 0.5rem;
  padding: 0.5rem;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.recent-searches-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  border-bottom: 1px solid rgba(131, 70, 255, 0.2);
  color: #c8c8c8;
}

.clear-searches {
  background: none;
  border: none;
  color: #8346ff;
  font-size: 0.8rem;
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  transition: color 0.2s ease;
}

.clear-searches:hover {
  color: #9666ff;
}

.recent-search-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  color: #ffffff;
}

.recent-search-item:hover {
  background: rgba(131, 70, 255, 0.1);
}

.remove-search {
  background: none;
  border: none;
  color: #666;
  font-size: 1.2rem;
  cursor: pointer;
  transition: color 0.2s ease;
}

.remove-search:hover {
  color: #ff4444;
}

/* Filter Components */
.filter-tags, .genre-filter {
  display: flex;
  gap: 1rem;
  margin: 2rem 0;
  flex-wrap: wrap;
  justify-content: center;
}

.genre-filter {
  border-top: 1px solid rgba(131, 70, 255, 0.2);
  padding: 1rem;
}

.filter-tag, .genre-btn {
  padding: 0.8rem 2rem;
  border-radius: 25px;
  border: none;
  background: rgba(131, 70, 255, 0.1);
  color: #c8c8c8;
  cursor: pointer;
  transition: all 0.3s ease;
}

.genre-btn {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.filter-tag:hover, .genre-btn:hover {
  background: rgba(131, 70, 255, 0.2);
  transform: translateY(-2px);
}

.filter-tag.active, .genre-btn.active {
  background: #8346ff;
  color: white;
  animation: pulse 1.5s infinite;
}

/* Results Grid */
.search-results {
  margin-top: 3rem;
}

.results-title {
  font-size: 1.8rem;
  margin-bottom: 2rem;
  text-align: center;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

/* Movie Card */
.movie-card, .poster-wrapper {
  position: relative;
}
.movie-card:hover .movie-title {
  color: #8346ff;
}

.poster-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  aspect-ratio: 2/3;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.movie-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0.8) 100%
  );
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.5rem;
  opacity: 0;
  transition: all 0.3s ease;
}


.poster-wrapper:hover {
  transform: translateY(-5px);
}
.poster-wrapper:hover .movie-overlay {
  opacity: 1;
}
.poster-wrapper:hover .movie-poster {
  transform: scale(1.1);
}
.movie-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.wish-btn {
  font-size: 1.2rem;
}

.wish-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    45deg,
    rgba(131, 70, 255, 0.2),
    rgba(79, 159, 255, 0.2)
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}
.wish-btn:hover {
  transform: scale(1.1);
  border-color: rgba(131, 70, 255, 0.5);
  box-shadow: 
    0 0 20px rgba(131, 70, 255, 0.3),
    0 0 40px rgba(131, 70, 255, 0.1);
}

.wish-btn:hover::before {
  opacity: 1;
}

.wish-btn.wished {
  background: rgba(131, 70, 255, 0.3);
  border-color: #8346ff;
}

.wish-icon {
  position: relative;
  z-index: 1;
  transition: transform 0.3s ease;
}

.action-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.action-btn:hover {
  transform: scale(1.1);
}

.action-btn:hover .wish-icon {
  transform: scale(1.1);
}

.detail-btn {
  background: linear-gradient(45deg, #8346ff, #4f9fff);
  border: none;
  color: white;
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.detail-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(131, 70, 255, 0.3);
}

/* 영화 제목 스타일 개선 */
.movie-title {
  margin-top: 1rem;
  font-size: 1rem;
  text-align: center;
  color: #ffffff;
  font-weight: 500;
  transition: color 0.3s ease;
}
/* Loading States */
.loading-more {
  text-align: center;
  padding: 2rem;
  color: #8346ff;
  font-size: 1.1rem;
  animation: bounce 1s infinite;
}

.no-results {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #c8c8c8;
}

/* Animations */
/* 애니메이션 추가 */
@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.wish-btn.wished .wish-icon {
  animation: heartBeat 0.3s ease-in-out;
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

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-container {
    padding: 1rem;
  }

  .search-container {
    flex-direction: column;
  }

  .search-button {
    padding: 1rem;
  }

  .results-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .recent-searches {
    position: fixed;
    top: auto;
    bottom: 0;
    left: 0;
    right: 0;
    margin: 0;
    border-radius: 15px 15px 0 0;
    max-height: 50vh;
    overflow-y: auto;
  }

  .genre-filter {
    padding: 0.5rem;
  }
  
  .genre-btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }

  .search-input {
    font-size: 1rem;
    padding: 0.8rem 1rem;
  }

  .results-title {
    font-size: 1.2rem;
    margin: 1rem 0;
  }
}
</style>