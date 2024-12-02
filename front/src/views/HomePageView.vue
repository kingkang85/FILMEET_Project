<template>
  <NavBar />
  <div class="home-page">
    <!-- Hero Section with Loading -->
    <section class="hero-section">
      <TransitionGroup name="fade">
        <!-- 로딩 상태 -->
        <div v-if="isLoading" key="hero-loading" class="hero-skeleton">
          <div class="hero-skeleton-content">
            <div class="skeleton-title"></div>
            <div class="skeleton-overview"></div>
            <div class="skeleton-meta">
              <div class="skeleton-rating"></div>
              <div class="skeleton-genre"></div>
            </div>
            <div class="skeleton-button"></div>
          </div>
        </div>
        
        <!-- 데이터가 있는 경우 -->
        <div v-else-if="featuredMovies && featuredMovies.length > 0" key="hero-content" class="hero-slider">
          <div 
            v-for="(movie, index) in featuredMovies" 
            :key="movie.id" 
            class="hero-slide"
            :style="{
              opacity: currentSlide === index ? '1' : '0',
              visibility: currentSlide === index ? 'visible' : 'hidden'
            }"
          >
            <div class="hero-backdrop">
              <img :src="movie.poster_path" :alt="movie.title" />
            </div>
            <div class="hero-content">
              <h1 class="hero-title">{{ movie.title }}</h1>
              <p class="hero-overview">{{ movie.overview }}</p>

              <div class="hero-meta">
                <span class="hero-rating">⭐ {{ movie.vote_average.toFixed(1) }}</span>
                
                <router-link :to="{ 
                  name: 'movielist', 
                  query: { 
                    filter: 'genre',
                    genreId: movie.genres[0]?.genre_id 
                  }
                }">
                <span class="hero-genre">{{ movie.genres[0]?.name }}</span>
                </router-link >
                <router-link
                v-if="movie.genres.length > 2" 
                :to="{ 
                  name: 'movielist', 
                  query: { 
                    filter: 'genre',
                    genreId: movie.genres[1]?.genre_id 
                  }
                }">
                <span class="hero-genre">{{ movie.genres[1]?.name }}</span>
                </router-link>
              </div>

              <div class="hero-buttons">
                <RouterLink :to="{ name: 'moviedetail', params: { id: movie.movie_id }}" class="hero-btn primary">
                  상세정보 보기
                </RouterLink>
              </div>
            </div>
          </div>
          <!-- Hero Navigation -->
          <div class="hero-navigation">
            <button class="hero-nav-btn prev" @click="prevSlide">‹</button>
            <div class="hero-dots">
              <button 
                v-for="(_, index) in featuredMovies"
                :key="index"
                :class="['hero-dot', { active: currentSlide === index }]"
                @click="currentSlide = index"
              ></button>
            </div>
            <button class="hero-nav-btn next" @click="nextSlide">›</button>
          </div>
        </div>
        
        <!-- 데이터가 없는 경우 -->
        <div v-else key="no-content" class="hero-empty">
          <p>표시할 영화가 없습니다.</p>
        </div>
      </TransitionGroup>
    </section>

    <div class="content-container">
      <!-- New Releases Section -->
      <section class="movies-section">
        <div class="section-header">
          <h2 class="section-title">NEW RELEASES</h2>
          <button @click="handleSeeMore('new')" class="see-more">
            더보기
            <span class="arrow">→</span>
          </button>
        </div>
        <div class="slider-container">
          <button class="slider-btn prev" @click="slideLeft('new')" :disabled="!canScrollLeft.new">‹</button>
          <div 
            class="movie-slider" 
            ref="newReleasesSlider"
            @scroll="updateScrollButtons('new')"
          >
            <TransitionGroup name="fade">
              <template v-if="isLoading">
                <div v-for="n in 6" :key="`new-skeleton-${n}`" class="movie-card">
                  <MovieSkeleton />
                </div>
              </template>
              <template v-else>
                <div 
                  v-for="(movie, index) in newReleases" 
                  :key="movie.id" 
                  class="movie-card"
                  :style="{ '--index': index }"
                >
                  <div class="poster-wrapper">
                    <img :src="movie.poster_path" :alt="movie.title" class="movie-poster" loading="lazy" />
                    <div class="movie-overlay">
                      <div class="movie-info">
                        <div class="movie-meta">
                          <span class="movie-rating">⭐ {{ movie.vote_average.toFixed(1) }}</span>
                          <span class="release-date">{{ formatDate(movie.release_date) }}</span>
                        </div>
                      </div>
                      <RouterLink 
                        :to="{ name: 'moviedetail', params: { id: movie.movie_id }}" 
                        class="detail-link"
                      >
                        <button class="detail-info-btn">
                          <span>상세정보 보기</span>
                        </button>
                      </RouterLink>
                    </div>
                  </div>
                  <h3 class="movie-title">{{ movie.title }}</h3>
                </div>
              </template>
            </TransitionGroup>
          </div>
          <button class="slider-btn next" @click="slideRight('new')" :disabled="!canScrollRight.new">›</button>
        </div>
      </section>

      <!-- Popular Movies Section -->
      <section class="movies-section">
        <div class="section-header">
          <h2 class="section-title">POPULAR NOW</h2>
          <button @click="handleSeeMore('popular')" class="see-more">
            더보기
            <span class="arrow">→</span>
          </button>
        </div>
        <div class="slider-container">
          <button class="slider-btn prev" @click="slideLeft('popular')" :disabled="!canScrollLeft.popular">‹</button>
          <div 
            class="movie-slider" 
            ref="popularSlider"
            @scroll="updateScrollButtons('popular')"
          >
            <TransitionGroup name="fade">
              <template v-if="isLoading">
                <div v-for="n in 6" :key="`popular-skeleton-${n}`" class="movie-card">
                  <MovieSkeleton />
                </div>
              </template>
              <template v-else>
                <div 
                  v-for="(movie, index) in popularMovies" 
                  :key="movie.id" 
                  class="movie-card"
                  :style="{ '--index': index }"
                >
                  <div class="poster-wrapper">
                    <img :src="movie.poster_path" :alt="movie.title" class="movie-poster" loading="lazy" />
                    <div class="movie-overlay">
                      <div class="movie-info">
                        <div class="movie-meta">
                          <span class="movie-rating">⭐ {{ movie.vote_average.toFixed(1) }}</span>
                          <span class="popularity">👥 {{ formatPopularity(movie.popularity) }}</span>
                        </div>
                      </div>
                      <RouterLink 
                        :to="{ name: 'moviedetail', params: { id: movie.movie_id }}" 
                        class="detail-link"
                      >
                        <button class="detail-info-btn">
                          <span>상세정보 보기</span>
                        </button>
                      </RouterLink>
                    </div>
                  </div>
                  <h3 class="movie-title">{{ movie.title }}</h3>
                </div>
              </template>
            </TransitionGroup>
          </div>
          <button class="slider-btn next" @click="slideRight('popular')" :disabled="!canScrollRight.popular">›</button>
        </div>
      </section>

      <!-- Top Rated Section -->
      <section class="movies-section">
        <div class="section-header">
          <h2 class="section-title">TOP RATED</h2>
          <button @click="handleSeeMore('top')" class="see-more">
            더보기
            <span class="arrow">→</span>
          </button>
        </div>
        <div class="slider-container">
          <button class="slider-btn prev" @click="slideLeft('top')" :disabled="!canScrollLeft.top">‹</button>
          <div 
            class="movie-slider" 
            ref="topRatedSlider"
            @scroll="updateScrollButtons('top')"
          >
            <TransitionGroup name="fade">
              <template v-if="isLoading">
                <div v-for="n in 6" :key="`top-skeleton-${n}`" class="movie-card">
                  <MovieSkeleton />
                </div>
              </template>
              <template v-else>
                <div 
                  v-for="(movie, index) in topRatedMovies" 
                  :key="movie.id" 
                  class="movie-card"
                  :style="{ '--index': index }"
                >
                  <div class="poster-wrapper">
                    <img :src="movie.poster_path" :alt="movie.title" class="movie-poster" loading="lazy" />
                    <div class="movie-overlay">
                      <div class="movie-info">
                        <div class="movie-meta">
                          <span class="movie-rating">⭐ {{ movie.vote_average.toFixed(1) }}</span>
                        </div>
                      </div>
                      <RouterLink 
                        :to="{ name: 'moviedetail', params: { id: movie.movie_id }}" 
                        class="detail-link"
                      >
                        <button class="detail-info-btn">
                          <span>상세정보 보기</span>
                        </button>
                      </RouterLink>
                    </div>
                  </div>
                  <h3 class="movie-title">{{ movie.title }}</h3>
                </div>
              </template>
            </TransitionGroup>
          </div>
          <button class="slider-btn next" @click="slideRight('top')" :disabled="!canScrollRight.top">›</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useMovieStore } from '@/stores/movie';
import { RouterLink, useRouter } from 'vue-router';
import NavBar from '@/components/common/NavBar.vue';
import MovieSkeleton from '@/components/MovieSkeleton.vue';

const movieStore = useMovieStore();
const router = useRouter();
const isLoading = ref(true);

// Hero section controls
const currentSlide = ref(0);
const autoplayInterval = ref(null);

const startAutoplay = () => {
  stopAutoplay(); // 기존 인터벌 제거
  autoplayInterval.value = setInterval(() => {
    nextSlide();
  }, 5000);
};

const stopAutoplay = () => {
  if (autoplayInterval.value) {
    clearInterval(autoplayInterval.value);
    autoplayInterval.value = null;
  }
};

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % featuredMovies.value.length;
};

const prevSlide = () => {
  currentSlide.value = currentSlide.value === 0 
    ? featuredMovies.value.length - 1 
    : currentSlide.value - 1;
};

// Slider refs and scroll state
const newReleasesSlider = ref(null);
const popularSlider = ref(null);
const topRatedSlider = ref(null);
const canScrollLeft = ref({ new: false, popular: false, top: false });
const canScrollRight = ref({ new: true, popular: true, top: true });

// Helper functions
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ko-KR', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
};

const formatPopularity = (popularity) => {
  return Math.round(popularity).toLocaleString();
};

// Scroll button update
const updateScrollButtons = (section) => {
  const slider = section === 'new' ? newReleasesSlider.value :
                section === 'popular' ? popularSlider.value :
                topRatedSlider.value;
  
  if (!slider) return;

  canScrollLeft.value[section] = slider.scrollLeft > 0;
  canScrollRight.value[section] = slider.scrollLeft < (slider.scrollWidth - slider.clientWidth - 1);
};

// Slider scroll functions with smooth behavior
const slideLeft = (section) => {
  const slider = section === 'new' ? newReleasesSlider.value :
                section === 'popular' ? popularSlider.value :
                topRatedSlider.value;
  
  if (!slider) return;
  
  const scrollAmount = slider.offsetWidth - 100; // 약간의 오버랩을 위해 100px 뺌
  slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
};

const slideRight = (section) => {
  const slider = section === 'new' ? newReleasesSlider.value :
                section === 'popular' ? popularSlider.value :
                topRatedSlider.value;
  
  if (!slider) return;
  
  const scrollAmount = slider.offsetWidth - 100;
  slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
};

// Computed movie lists
const featuredMovies = computed(() => {
  if (!movieStore.movies?.length) return [];
  
  console.log('전체 영화:', movieStore.movies.length);
  
  const filtered = movieStore.movies
    .filter(movie => {
      // 필수 데이터만 체크
      const hasGoodRating = movie.vote_average > 6;
      const hasPoster = Boolean(movie.poster_path);
      const hasOverview = Boolean(movie.overview?.trim());
      
      return hasGoodRating && hasPoster && hasOverview;
    })
    .sort((a, b) => b.popularity - a.popularity)
    .slice(0, 5);
    
  console.log('필터링된 영화:', filtered.length);
  
  return filtered;
});

const newReleases = computed(() => {
  if (!movieStore.movies) return [];
  return [...movieStore.movies]
    .sort((a, b) => new Date(b.release_date) - new Date(a.release_date))
    .slice(0, 12);
});

const popularMovies = computed(() => {
  if (!movieStore.movies) return [];
  return [...movieStore.movies]
    .sort((a, b) => b.popularity - a.popularity)
    .slice(0, 12);
});

const topRatedMovies = computed(() => {
  if (!movieStore.movies) return [];
  return [...movieStore.movies]
    .sort((a, b) => b.vote_average - a.vote_average)
    .slice(0, 12);
});

const handleSeeMore = (filter) => {
  router.push({
    name: 'movielist',
    query: { filter }
  });
};

// Lifecycle hooks
onMounted(async () => {
  try {
    if (!movieStore.movies.length) {
      await movieStore.fetchMovies();
    }
    startAutoplay();
  } catch (error) {
    console.error('Failed to fetch movies:', error);
  } finally {
    setTimeout(() => {
      isLoading.value = false;
    }, 400); // 최소 로딩 시간 보장
  }
});

onBeforeUnmount(() => {
  stopAutoplay();
});
</script>

<style scoped>
.home-page {
  background-color: #0b001a;
  min-height: 100vh;
  color: white;
}

/* Content Container */
.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* Hero Section Styles */
.hero-section {
  height: 600px; /* 높이 조정 */
  position: relative;
  overflow: hidden;
  background-color: #0b001a;
  padding: 2rem 0;
}

.hero-slider {
  position: relative;
  height: 100%;
}

.hero-slide {
  position: absolute;
  width: 100%;
  max-width: 1200px; /* 최대 너비 제한 */
  height: 100%;
  left: 50%;
  transform: translateX(-50%);
  display: grid;
  grid-template-columns: auto 1fr; /* 이미지 크기에 맞추고 나머지 공간 사용 */
  gap: 3rem;
  padding: 0 2rem;
  align-items: center;
}

.hero-backdrop {
  position: relative;
  height: 100%;
  width: 400px; /* 포스터 너비 고정 */
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.hero-backdrop img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 100; /* 투명도 제거 */
}
/* .hero-section::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgba(11, 0, 26, 0.9) 0%,
    rgba(11, 0, 26, 0.8) 50%,
    rgba(11, 0, 26, 0.9) 100%
  );
  z-index: 1;
} */

.hero-content {
  position: relative;
  z-index: 2;
  padding: 2rem;
  color: white;
  max-width: 600px;
}

.hero-title {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
  background: linear-gradient(45deg, #ffffff, #8346ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-overview {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.hero-meta {
  display: flex;
  gap: 0.8rem;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.hero-rating, 
.hero-genre {
 display: inline-block;
 padding: 0.5rem 1rem;
 margin-right: 0.5rem;
 margin-bottom: 0.8rem;
 background: rgba(131, 70, 255, 0.1); 
 border: 1px solid rgba(131, 70, 255, 0.2);
 border-radius: 20px;
 color: #fff;
 font-size: 0.9rem;
 transition: all 0.3s ease;
}
.hero-genre:hover {
 background: rgba(131, 70, 255, 0.2);
 border-color: #8346ff;
 transform: translateY(-2px);
 box-shadow: 0 4px 15px rgba(131, 70, 255, 0.2);
}
.hero-genre.active {
 background: #8346ff;
 border-color: #8346ff;
 box-shadow: 0 4px 15px rgba(131, 70, 255, 0.3);
}
.hero-genre {
 position: relative;
 overflow: hidden;
}

.hero-genre::before {
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

.hero-genre:hover::before {
 transform: translateX(100%);
}
a + a {
 margin-left: 0.5rem;
}
.hero-rating {
  background: rgba(131, 70, 255, 0.2);
}

.hero-genre {
  background: rgba(255, 255, 255, 0.1);
}

.hero-buttons {
  display: flex;
  gap: 1rem;
}

.hero-btn {
  padding: 1rem 2rem;
  border-radius: 30px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.hero-btn.primary {
  background: linear-gradient(45deg, #8346ff, #4f9fff);
  color: white;
  border: none;
}

.hero-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(131, 70, 255, 0.3);
}

/* Section Styles */
.movies-section {
  margin-bottom: 4rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  position: relative;
}

.section-header::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(
    to right,
    rgba(131, 70, 255, 0.5) 0%,
    rgba(131, 70, 255, 0.2) 100%
  );
}

.section-title {
  font-size: 2.2rem;
  font-weight: 700;
  letter-spacing: 1px;
  background: linear-gradient(45deg, #ffffff 30%, #8346ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Slider Styles */
.slider-container {
  position: relative;
  padding: 0 2rem;
}

.movie-slider {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 1rem 0;
  scrollbar-width: none;
  -ms-overflow-style: none;
  position: relative; /* 추가 */
  perspective: 1000px; /* 3D 효과를 위한 perspective 추가 */
}
.movie-slider::-webkit-scrollbar {
  display: none;
}

/* Movie Card Styles */
.movie-card {
  flex: 0 0 200px;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease forwards;
  animation-delay: calc(var(--index) * 0.1s);
  will-change: transform, opacity; /* 성능 최적화 */
}

.poster-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 2/3;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.movie-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.4),
    rgba(0, 0, 0, 0.9)
  );
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 1.5rem;
  opacity: 0;
  transition: all 0.3s ease;
}

.movie-info {
  margin-bottom: 1rem;
}

.movie-meta {
  display: flex;
  gap: 0.8rem;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.movie-rating,
.popularity {
  padding: 0.4rem 0.8rem;
  background: rgba(131, 70, 255, 0.2);
  border-radius: 20px;
  backdrop-filter: blur(4px);
}

.detail-link {
  width: 100%;
  text-decoration: none;
}

.detail-info-btn {
  width: 100%;
  padding: 0.8rem;
  background: rgba(131, 70, 255, 0.9);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detail-info-btn:hover {
  background: rgba(150, 102, 255, 0.95);
  transform: scale(1.02);
}

.movie-title {
  margin-top: 1rem;
  font-size: 1rem;
  text-align: center;
  color: white;
}

/* Hover Effects */
.movie-card:hover {
  transform: translateY(-5px);
}

.movie-card:hover .movie-overlay {
  opacity: 1;
}

.movie-card:hover .movie-poster {
  transform: scale(1.05);
}
.hero-empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.2rem;
}
/* Navigation Buttons */
.hero-navigation {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  max-width: 1200px;
  padding: 0 2rem;
  justify-content: center;
}
.hero-nav-btn,
.slider-btn {
  background: rgba(131, 70, 255, 0.2);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.slider-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}

.slider-btn:hover:not(:disabled),
.hero-nav-btn:hover {
  background: rgba(131, 70, 255, 0.4);
}

.slider-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.slider-btn.prev { left: 0; }
.slider-btn.next { right: 0; }

.hero-dots {
  display: flex;
  gap: 0.5rem;
}

.hero-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.hero-dot.active {
  background: #8346ff;
  transform: scale(1.2);
}

/* Animations */
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

/* Loading States */
.hero-skeleton {
  width: 100%;
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 3rem;
  padding: 0 2rem;
  align-items: center;
}
.hero-skeleton-content {
  width: 100%;
  max-width: 600px;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton-title,
.skeleton-overview,
.skeleton-meta,
.skeleton-button,
.skeleton-rating,
.skeleton-genre {
  background: linear-gradient(
    90deg,
    rgba(131, 70, 255, 0.05) 25%,
    rgba(131, 70, 255, 0.15) 50%,
    rgba(131, 70, 255, 0.05) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 2s infinite linear;
  border-radius: 8px;
}

.skeleton-title {
  height: 60px;
  width: 80%;
  margin-bottom: 2rem;
}

.skeleton-overview {
  height: 80px;
  width: 100%;
  margin-bottom: 2rem;
}

.skeleton-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.skeleton-rating,
.skeleton-genre {
  height: 40px;
  width: 120px;
  border-radius: 20px;
}

.skeleton-button {
  height: 50px;
  width: 200px;
  border-radius: 25px;
}

/* Transitions */
.fade-move,
.fade-enter-active,
.fade-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

.fade-leave-active {
  position: absolute;
}

/* See More Button */
.see-more {
  color: #8346ff;
  background: none;
  border: none;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.see-more:hover {
  color: #9666ff;
  transform: translateX(5px);
}

.see-more .arrow {
  transition: transform 0.3s ease;
}

.see-more:hover .arrow {
  transform: translateX(5px);
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .hero-slide {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .hero-backdrop {
    width: 300px;
    height: 450px;
    margin: 0 auto;
  }

  .hero-content {
    text-align: center;
    padding: 1rem;
  }
}
@media (max-width: 768px) {
  .hero-section {
    height: 70vh;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-content {
    margin-left: 5%;
    padding: 1rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .slider-btn {
    display: none;
  }
  
  .movie-slider {
    padding: 0;
  }
  
  .hero-skeleton {
    padding: 0 5%;
  }
  
  .skeleton-title {
    height: 40px;
    margin-bottom: 1.5rem;
  }
  
  .skeleton-overview {
    height: 60px;
    margin-bottom: 1.5rem;
  }
  
  .skeleton-rating,
  .skeleton-genre {
    height: 35px;
    width: 100px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-overview {
    font-size: 1rem;
    -webkit-line-clamp: 2;
  }

  .hero-buttons {
    flex-direction: column;
  }

  .section-title {
    font-size: 1.5rem;
  }
}

</style>