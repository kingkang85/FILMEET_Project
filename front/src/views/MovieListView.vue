<template>
  <div class="movie-list">
    <NavBar />
    <div class="content-wrapper">
      <!-- 검색바 개선 -->
      <div class="search-container">
        <div class="search-wrapper">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="영화를 검색해보세요..."
            class="search-input"
            @input="handleSearch"
          >
          <button class="search-btn" @click="handleSearch">
            <span class="search-icon">🔍</span>
          </button>
        </div>
      </div>

      <!-- 필터 섹션 -->
        <div class="filter-container">
        <!-- 장르 필터 -->
        <div class="genre-filter">
          <div class="genre-buttons">
            <button 
              v-for="genre in allGenreList" 
              :key="genre.id"
              :class="['genre-btn', { active: selectedGenreId === genre.id }]"
              @click="selectGenre(genre.id)"
            >
              {{ genre.name }}
            </button>
          </div>
        </div>

        <!-- 정렬 옵션 -->
        <div class="sort-filter">
          <div class="sort-buttons-wrapper">
            <button 
              v-for="option in sortOptions" 
              :key="option.id"
              :class="['genre-btn', { active: option.active }]"
              @click="setSortOption(option)"
            >
              {{ option.name }}
            </button>
          </div>
        </div>
      </div>

      <!-- 메인 컨텐츠 -->
      <div class="movies-section">
        <!-- 로딩 상태 -->
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>영화 정보를 불러오는 중...</p>
        </div>

          <TransitionGroup 
            name="movie-grid"
            tag="div"
            class="movies-section"
            :css="false"
            @before-enter="beforeEnter"
            @enter="enter"
            @leave="leave"
          >
          <!-- Loading Skeletons -->
          <div v-if="isLoading" key="skeletons" class="movies-grid">
            <MovieSkeleton v-for="n in 15" :key="`skeleton-${n}`" />
          </div>

  <!-- Movie Grid -->
  <div v-else-if="filteredMovies.length" key="movies" class="movies-grid">
    <!-- 여기서 중첩된 TransitionGroup 제거 -->
    <div 
      v-for="(movie, index) in paginatedMovies" 
      :key="movie.id" 
      class="movie-card"
      :style="{ animationDelay: `${index * 0.05}s` }"
    >
      <div class="movie-poster-wrapper">
        <img 
          :src="movie.poster_path" 
          :alt="movie.title" 
          class="movie-poster"
          loading="lazy"
        />
        <div class="movie-overlay">
          <div class="movie-actions">
            <button 
              @click.stop="handleWish(movie)"
              :class="['action-btn wish-btn', { 'wished': isMovieWished(movie.movie_id) }]"
              :title="isMovieWished(movie.movie_id) ? '찜 해제' : '찜하기'"
            >
              <span class="wish-icon">
                {{ isMovieWished(movie.movie_id) ? '❤️' : '🤍' }}
              </span>
            </button>
            <button 
              class="action-btn" 
              title="리뷰"
              @click.prevent="openDiscussion(movie.movie_id)"
            >
              <span class="action-icon">💬</span>
            </button>
          </div>
          <router-link :to="{ name: 'moviedetail', params: { id: movie.movie_id }}">
            <button class="detail-btn">
              <span>상세정보 보기</span>
            </button>
          </router-link>
        </div>
      </div>
      <h3 class="movie-title">{{ movie.title }}</h3>
      <div class="movie-info">
        <span class="movie-year">{{ new Date(movie.release_date).getFullYear() }}</span>
        <span class="movie-rating">⭐ {{ movie.vote_average.toFixed(1) }}</span>
      </div>
    </div>
  </div>

        <!-- No Results Message -->
        <div v-else key="no-results" class="no-results">
          검색 결과가 없습니다 😢
        </div>
        <!-- 결과 없음 -->
        <div v-else class="no-results">
          <span class="no-results-emoji">😢</span>
          <p>검색 결과가 없습니다</p>
        </div>
      </TransitionGroup>

        <!-- 페이지네이션 -->
        <div v-if="totalPages > 1" class="pagination-wrapper">
          <div class="pagination">
            <button 
              class="page-btn prev"
              @click="previousPage"
              :disabled="currentPage === 1"
            >
              이전
            </button>
            <div class="page-numbers">
              <button 
                v-for="n in displayedPageNumbers" 
                :key="n"
                :class="['page-number', { active: n === currentPage }]"
                @click="goToPage(n)"
              >
                {{ n }}
              </button>
            </div>
            <button 
              class="page-btn next"
              @click="nextPage"
              :disabled="currentPage === totalPages"
            >
              다음
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
    <!-- Discussion Modal 추가 -->
    <DiscussionModal 
    v-if="selectedMovieId"
    :is-open="showDiscussionModal"
    :movie-id="selectedMovieId"
    @close="closeDiscussion"
  />
</template>

<script setup>
import NavBar from '@/components/common/NavBar.vue'
import { useMovieStore } from '@/stores/movie'
import { useWishStore } from '@/stores/wishlist'
import { ref, computed, onMounted, watch } from 'vue'
import { TransitionGroup } from 'vue'
import { useRoute } from 'vue-router'
import MovieSkeleton from '@/components/MovieSkeleton.vue'
import DiscussionModal from '@/components/DiscussionModal.vue';
import { useRouter } from 'vue-router';
const route = useRoute();
const router = useRouter();
const movieStore = useMovieStore();
const wishStore = useWishStore()
const currentPage = ref(1);
const itemsPerPage = 16;
const isLoading = ref(true);
const searchQuery = ref('');
const selectedGenreId = ref(null);

// 장르 목록 (전체 옵션 추가)
const allGenreList = [
  { id: null, name: '전체' },
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
  { id: 10770, name: 'TV 영화' },
  { id: 53, name: '스릴러' },
  { id: 10752, name: '전쟁' },
  { id: 37, name: '서부' }
];

// 정렬 옵션
const sortOptions = ref([
  { id: 1, name: '추천순', type: 'top', active: true },
  { id: 2, name: '인기순', type: 'popular', active: false },
  { id: 3, name: '개봉순', type: 'new', active: false },
]);

// 정렬 옵션 선택 함수
const setSortOption = (selectedOption) => {
  sortOptions.value.forEach(option => {
    option.active = option.id === selectedOption.id;
  });
  currentPage.value = 1;  // 페이지 초기화
};

// Discussion Modal 관련 상태
const showDiscussionModal = ref(false);
const selectedMovieId = ref(null);

// Discussion Modal 열기/닫기
const openDiscussion = (movieId) => {
  selectedMovieId.value = movieId;
  showDiscussionModal.value = true;
};

const closeDiscussion = () => {
  showDiscussionModal.value = false;
  selectedMovieId.value = null;
};

// URL query로부터 필터 설정
const setFilterFromQuery = () => {
  const filterType = route.query.filter;
  const genreId = route.query.genreId ? Number(route.query.genreId) : null;

  if (filterType === 'genre') {
    selectedGenreId.value = genreId;
  }
};

// route.query 변경 감지
watch(
  () => route.query,
  () => {
    setFilterFromQuery();
  },
  { immediate: true }
);

// genre ID 변경 감지
watch(
  () => route.query.genreId,
  (newGenreId) => {
    if (newGenreId) {
      selectedGenreId.value = Number(newGenreId);
    }
  }
);

// 검색 및 필터링된 영화 목록
const filteredMovies = computed(() => {
  if (!movieStore.movies) return [];
  
  let filtered = [...movieStore.movies];
  
  // 장르 필터링 (전체가 아닌 경우에만)
  if (selectedGenreId.value !== null) {
    filtered = filtered.filter(movie => 
      movie.genres?.some(genre => genre.genre_id === selectedGenreId.value)
    );
  }
  
  // 검색어 필터링 추가
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(movie => 
      movie.title.toLowerCase().includes(query)
    );
  }
  
  // 정렬 옵션 적용
  const activeSort = sortOptions.value.find(option => option.active);
  if (activeSort) {
    switch(activeSort.type) {
      case 'popular':
        filtered.sort((a, b) => b.popularity - a.popularity);
        break;
      case 'new':
        filtered.sort((a, b) => new Date(b.release_date) - new Date(a.release_date));
        break;
      case 'top':
        filtered.sort((a, b) => b.vote_average - a.vote_average);
        break;
    }
  }
  
  return filtered;
});

// 페이지네이션 관련 computed 속성들
const totalPages = computed(() => {
  return Math.ceil(filteredMovies.value.length / itemsPerPage);
});

const paginatedMovies = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredMovies.value.slice(start, end);
});

const displayedPageNumbers = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  const pages = [];
  
  if (total <= 5) {
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
  } else {
    let start = Math.max(current - 2, 1);
    let end = Math.min(start + 4, total);
    
    if (end === total) {
      start = Math.max(end - 4, 1);
    }
    
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
  }
  
  return pages;
});

// 필터 변경시 페이지 초기화를 위한 watch
watch([searchQuery, selectedGenreId], () => {
  currentPage.value = 1;
});

// 장르 선택
const selectGenre = (genreId) => {
  selectedGenreId.value = selectedGenreId.value === genreId ? null : genreId;
  currentPage.value = 1;
};

// 검색 핸들러 (디바운스 처리)
let searchTimeout;
const handleSearch = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    currentPage.value = 1;
  }, 300);
};

// 페이지 이동 함수들
const goToPage = (page) => {
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

// 컴포넌트 마운트시 위시리스트 가져오기
onMounted(async () => {
  isLoading.value = true;
  try {
    await Promise.all([
      wishStore.getMovieWishlist()
    ])
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    isLoading.value = false
  }
});

// 찜하기
const handleWish = async (movie) => {
  if (!movie) return;

  try {
    const status = await wishStore.wishMovie(movie.movie_id);
    if (status === 'added') {
      alert('찜 목록에 추가되었습니다.');
    } else {
      alert('찜 목록에서 제거되었습니다.');
    }
  } catch (err) {
    console.error('Wish error:', err);
    if (err.response?.status === 401) {
      alert('로그인이 필요합니다.');
    }
      router.push('/login');
  }
};


const isMovieWished = (movieId) => {
  return wishStore.isMovieInWishlist(movieId)
}
</script>

<style>
/* Base Layout */
.movie-list {
  background-color: #0b001a;
  min-height: 100vh;
  color: white;
  padding-bottom: 4rem;
}

.content-wrapper {
  padding-top: 2rem;
}

/* Search Section */
.search-container {
  max-width: 1200px;
  margin: 0 auto 2rem;
  padding: 0 2rem;
}

.search-wrapper {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50px;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  border: 1px solid rgba(131, 70, 255, 0.2);
  transition: all 0.3s ease;
}

.search-wrapper:focus-within {
  border-color: #8346ff;
  box-shadow: 0 0 0 3px rgba(131, 70, 255, 0.2);
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 0.8rem 1.5rem;
  color: white;
  font-size: 1rem;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-btn {
  background: #8346ff;
  border: none;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn:hover {
  background: #9666ff;
  transform: scale(1.05);
}

/* Filter Section */
.filter-container {
  max-width: 1200px;
  margin: 0 auto 2rem;
  padding: 2rem;
  background: rgba(131, 70, 255, 0.05);
  border-radius: 16px;
  border: 1px solid rgba(131, 70, 255, 0.1);
}

.filter-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #8346ff;
}

.filter-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.filter-btn {
  background: rgba(131, 70, 255, 0.1);
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 50px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(131, 70, 255, 0.2);
}

.filter-btn:hover {
  background: rgba(131, 70, 255, 0.2);
  transform: translateY(-2px);
}

.filter-btn.active {
  background: #8346ff;
  box-shadow: 0 4px 15px rgba(131, 70, 255, 0.3);
}

/* Genre Section */
.genre-filter {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(131, 70, 255, 0.1);
}

.genre-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
}

.genre-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(131, 70, 255, 0.1);
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.genre-btn:hover {
  background: rgba(131, 70, 255, 0.1);
  transform: translateY(-2px);
}

.genre-btn.active {
  background: #8346ff;
  border-color: #8346ff;
  box-shadow: 0 4px 15px rgba(131, 70, 255, 0.3);
}

/* Sort Section */
.sort-filter {
  padding-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-top: 1px solid rgba(131, 70, 255, 0.1);
}

.sort-buttons-wrapper {
  display: flex;
  justify-content: center;  /* 가운데 정렬 */
  flex-wrap: wrap;
  gap: 0.8rem;
  width: 100%;
  max-width: 600px;  /* 최대 너비 설정 */
  margin: 0 auto;
}

.sort-buttons {
  display: flex;
  gap: 1rem;
}

.sort-btn:hover {
  background: rgba(131, 70, 255, 0.2);
  transform: translateY(-2px);
}

.sort-btn.active {
  background: #8346ff;
  box-shadow: 0 4px 15px rgba(131, 70, 255, 0.3);
}

/* Movies Grid */
.movies-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.movie-card {
  animation: fadeIn 0.5s ease forwards;
  opacity: 0;
}

.movie-poster-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 2/3;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
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
  background: rgba(11, 0, 26, 0.85);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.5rem;
  opacity: 0;
  transition: all 0.3s ease;
}

.movie-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
}

.action-btn {
  background: rgba(131, 70, 255, 0.2);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(131, 70, 255, 0.4);
  transform: scale(1.1);
}

.wish-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
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

.detail-btn {
  background: #8346ff;
  border: none;
  width: 100%;
  padding: 1rem;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detail-btn:hover {
  background: #9666ff;
  transform: translateY(-2px);
}

.movie-title {
  margin-top: 1rem;
  text-align: center;
  font-size: 1rem;
  font-weight: 500;
}

.movie-info {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #888;
}

/* Hover Effects */
.movie-poster-wrapper:hover {
  transform: translateY(-5px);
}

.movie-poster-wrapper:hover .movie-overlay {
  opacity: 1;
}

.movie-poster-wrapper:hover .movie-poster {
  transform: scale(1.1);
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 3rem;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(131, 70, 255, 0.3);
  border-top-color: #8346ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

/* No Results */
.no-results {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.no-results-emoji {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

/* Pagination */
.pagination-wrapper {
  margin-top: 3rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.page-numbers {
  display: flex;
  gap: 0.5rem;
}

.page-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 50%;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-number.active {
  background: #8346ff;
  border-color: #8346ff;
}

.page-number:hover:not(.active) {
  background: rgba(131, 70, 255, 0.2);
  transform: translateY(-2px);
}

.page-btn {
  padding: 0.8rem 1.5rem;
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 25px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:not(:disabled):hover {
  background: rgba(131, 70, 255, 0.2);
  transform: translateY(-2px);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Animations */
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

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.wish-btn.wished .wish-icon {
  animation: heartBeat 0.3s ease-in-out;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.movie-grid-move {
  transition: transform 0.5s ease;
}

.movie-grid-enter-active,
.movie-grid-leave-active {
  transition: all 0.5s ease;
}

.movie-grid-enter-from,
.movie-grid-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* Custom Scrollbar */
.movies-section::-webkit-scrollbar {
  width: 8px;
}

.movies-section::-webkit-scrollbar-track {
  background: rgba(131, 70, 255, 0.1);
  border-radius: 4px;
}

.movies-section::-webkit-scrollbar-thumb {
  background: rgba(131, 70, 255, 0.3);
  border-radius: 4px;
  transition: background 0.3s ease;
}

.movies-section::-webkit-scrollbar-thumb:hover {
  background: rgba(131, 70, 255, 0.5);
}

/* Utility Classes */
.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hover-scale {
  transition: transform 0.3s ease;
}

.hover-scale:hover {
  transform: scale(1.05);
}

.hover-lift {
  transition: transform 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-5px);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .movies-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 992px) {
  .movies-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }

  .search-container,
  .filter-container,
  .movies-section {
    padding: 0 1.5rem;
  }

  .movie-title {
    font-size: 0.9rem;
  }

  .sort-filter {
    padding: 1.5rem 0;
  }
}

@media (max-width: 768px) {
  .movies-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.2rem;
  }

  .search-container,
  .filter-container,
  .movies-section {
    padding: 0 1rem;
  }

  .search-wrapper {
    width: 100%;
  }

  .filter-buttons,
  .genre-buttons,
  .sort-buttons {
    justify-content: center;
  }

  .filter-btn,
  .sort-btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }

  .genre-btn {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
  }

  .movie-actions {
    gap: 0.5rem;
  }

  .action-btn {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }

  .detail-btn {
    padding: 0.8rem;
    font-size: 0.9rem;
  }

  .pagination {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.8rem;
  }

  .page-number {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }

  .page-btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .movie-list {
    padding-bottom: 2rem;
  }

  .content-wrapper {
    padding-top: 1rem;
  }

  .search-input {
    font-size: 0.9rem;
    padding: 0.6rem 1rem;
  }

  .search-btn {
    width: 40px;
    height: 40px;
  }

  .movies-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .movie-poster-wrapper {
    border-radius: 8px;
  }

  .movie-overlay {
    padding: 1rem;
  }

  .movie-title {
    font-size: 0.85rem;
    margin-top: 0.8rem;
  }

  .movie-info {
    font-size: 0.8rem;
    gap: 0.8rem;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
  }

  .no-results-emoji {
    font-size: 2.5rem;
  }

  .sort-filter {
    padding: 1.5rem 0;
  }
}

/* 반응형 조정 */
@media (max-width: 768px) {
  .sort-filter {
    padding: 1.5rem 0; 
  }
  
  .sort-buttons-wrapper {
    padding: 0 1rem;
  }
}
</style>