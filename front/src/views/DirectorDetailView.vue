<template>
  <div class="director-detail">
    <NavBar />
    
    <div v-if="isLoading" class="loading-skeleton">
      <MovieSkeleton />
    </div>

    <div v-else-if="director" class="content-container">
      <div class="profile-section">
        <div class="profile-image-container">
          <img 
            :src="getImageUrl(director.profile_path)"
            :alt="director.name"
            class="profile-image"
          />
          <button 
            @click="handleWish"
            :class="['wish-btn', { 'wished': isWished }]"
            :title="isWished ? '찜 해제' : '찜하기'"
          >
            <span class="wish-icon">{{ isWished ? '❤️' : '🤍' }}</span>
          </button>
        </div>
        
        <div class="profile-info">
          <h1 class="director-name">{{ director.name }}</h1>
          
          <div class="info-content">
            <div class="info-item">
              <span class="label">생년월일</span>
              <span class="value">{{ formatDate(director.birth_date) }}</span>
            </div>
            <div class="info-item">
              <span class="label">출생</span>
              <span class="value">{{ director.birthplace || '정보 없음' }}</span>
            </div>
            <div class="info-item">
              <span class="label">직업</span>
              <span class="value">감독</span>
            </div>
          </div>

          <div v-if="director.biography" class="biography">
            <div class="biography-header">
              <h3 class="biography-title">약력</h3>
              <button @click="toggleBiography" class="toggle-btn">
                {{ isExpanded ? '접기' : '더보기' }}
              </button>
            </div>
            <p class="biography-text" :class="{ 'expanded': isExpanded }">
              {{ director.biography }}
            </p>
          </div>
        </div>
      </div>

      <div class="filmography-section">
        <h2 class="section-title">FILMOGRAPHY</h2>
        <div class="movies-grid">
          <router-link 
            v-for="movie in director.filmography" 
            :key="movie.movie_id"
            :to="{ name: 'moviedetail', params: { id: movie.movie_id }}"
            class="movie-card"
          >
            <div class="poster-wrapper">
              <img :src="movie.poster_path" :alt="movie.title" class="movie-poster" />
              <div class="movie-overlay">
                <p class="release-date">{{ formatDate(movie.release_date) }}</p>
              </div>
            </div>
            <h4 class="movie-title">{{ movie.title }}</h4>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWishStore } from '@/stores/wishlist'
import NavBar from '@/components/common/NavBar.vue'
import MovieSkeleton from '@/components/MovieSkeleton.vue'
import axios from 'axios'

const wishStore = useWishStore()
const route = useRoute()
const router = useRouter()
const director = ref(null)
const isLoading = ref(true)
const error = ref(null)

const fetchDirectorData = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/movies/directors/${route.params.id}/`);
    console.log(response.data)
    director.value = response.data;
  } catch (err) {
    error.value = err.message;
    console.error('Error fetching director details:', err);
  } finally {
    isLoading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '정보 없음';
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const isWished = computed(() => {
  if (!director.value?.person_id) return false
  return wishStore.isDirectorInWishlist(director.value.person_id)
})

onMounted(async () => {
  if (route.params.id) {
    try {
      await Promise.all([
        fetchDirectorData(),
        wishStore.getDirectorWishlist()
      ])
    } catch (err) {
      console.error('Error initializing data:', err)
    }
  }
})

const handleWish = async () => {
  if (!director.value) return

  try {
    const status = await wishStore.wishDirector(director.value.person_id)
    if (status === 'added') {
      alert('찜 목록에 추가되었습니다.')
    } else {
      alert('찜 목록에서 제거되었습니다.')
    }
  } catch (err) {
    console.log(err)
    if (err.response?.status === 401) {
      alert('로그인이 필요합니다.');
    }
      router.push('/login');
  }
}
const isExpanded = ref(false)
const biographyText = ref(null)

const toggleBiography = () => {
  isExpanded.value = !isExpanded.value
}

const baseURL = 'http://127.0.0.1:8000'

const getImageUrl = (imagePath) => {
  // TMDB 이미지인 경우 (http로 시작하는 전체 URL)
  if (imagePath?.startsWith('http')) {
    return imagePath
  }
  // 이미지가 없는 경우 기본 이미지 반환
  return baseURL + '/static/images/default_profile.jpg'
}
</script>

<style scoped>
.director-detail {
  min-height: 100vh;
  background-color: #0b001a;
  color: white;
  padding-top: 2rem;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.profile-section {
  display: flex;
  gap: 3rem;
  margin-bottom: 4rem;
  background: rgba(131, 70, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
}

.profile-image-container {
  position: relative;
  width: 320px;
  flex-shrink: 0;
}

.profile-image {
  width: 100%;
  height: auto;
  aspect-ratio: 3/4;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.wish-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.6);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  width: 46px;
  height: 46px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
}

.wish-btn:hover {
  transform: scale(1.1);
  border-color: #8346ff;
  box-shadow: 0 0 15px rgba(131, 70, 255, 0.3);
}

.wish-btn.wished {
  background: rgba(131, 70, 255, 0.3);
  border-color: #8346ff;
}

.wish-icon {
  font-size: 1.5rem;
}

.profile-info {
  flex: 1;
}

.director-name {
  font-size: 2.8rem;
  margin-bottom: 2rem;
  background: linear-gradient(45deg, #ffffff, #8346ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 700;
}

.info-content {
  background: rgba(131, 70, 255, 0.03);
  border-radius: 8px;
  padding: 1.5rem;
}

.info-item {
  display: flex;
  gap: 2rem;
  padding: 0.8rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  min-width: 100px;
  color: #8346ff;
  font-weight: 500;
}

.value {
  color: #e5e5e5;
}

.biography {
  margin-top: 1.5rem;
  background: rgba(131, 70, 255, 0.03);
  border-radius: 8px;
  padding: 1.5rem;
}

.biography-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.biography-title {
  font-size: 1.3rem;
  color: #8346ff;
  margin: 0;
  font-weight: 600;
}

.toggle-btn {
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.3);
  color: #8346ff;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.toggle-btn:hover {
  background: rgba(131, 70, 255, 0.2);
  transform: translateY(-2px);
}

.biography-text {
  line-height: 1.7;
  color: #e5e5e5;
  max-height: 4.5em;
  overflow: hidden;
  transition: all 0.3s ease;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.biography-text.expanded {
  max-height: none;
  -webkit-line-clamp: unset;
}

.filmography-section {
  padding-top: 2rem;
  text-align: center;
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 3rem;
  background: linear-gradient(to right, #ffffff, #8346ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: bold;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 2rem;
}

.movie-card {
  text-decoration: none;
  color: white;
  transition: 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.poster-wrapper {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 2/3;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.movie-card:hover .movie-poster {
  transform: scale(1.05);
}

.movie-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  opacity: 0;
  transition: 0.3s ease;
  display: flex;
  align-items: flex-end;
  padding: 1rem;
}

.movie-card:hover .movie-overlay {
  opacity: 1;
}

.release-date {
  color: #a78bfa;
  margin: 0;
  font-size: 0.9rem;
}

.movie-title {
  margin: 0.8rem 0 0;
  font-size: 0.95rem;
  transition: color 0.3s ease;
}

.movie-card:hover .movie-title {
  color: #8346ff;
}

@media (max-width: 768px) {
  .content-container {
    padding: 0 1rem;
  }

  .profile-section {
    flex-direction: column;
    gap: 2rem;
  }

  .profile-image-container {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
  }

  .director-name {
    text-align: center;
    font-size: 2rem;
  }

  .movies-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .info-content, .biography {
    margin-top: 1rem;
  }
}
</style>