<template>
  <div class="wishlist-container">
    <NavBar />
    <div class="content-wrapper">
      <div class="header-section">
        <h1 class="page-title">찜한 감독 목록</h1>
        <div class="sort-options">
          <button 
            v-for="option in sortOptions" 
            :key="option.id"
            :class="['sort-btn', { active: option.active }]"
            @click="setSortOption(option)"
          >
            {{ option.name }}
          </button>
        </div>
      </div>

      <div class="directors-grid" v-if="sortedDirectors?.length">
        <div 
          v-for="director in sortedDirectors" 
          :key="director.person_id" 
          class="director-card"
        >
          <div class="director-poster-wrapper">
            <img 
              :src="director.profile_path" 
              :alt="director.name" 
              class="director-poster"
              loading="lazy"
            />
            <div class="movie-overlay">
              <div class="movie-actions">
                <button 
                  class="action-btn" 
                  @click="handleWish(director)"
                  title="찜 취소"
                >
                  🗑️
                </button>
              </div>
              <router-link 
                :to="{ name: 'directordetail', params: { id: director.person_id }}"
                class="detail-link"
              >
                <button class="detail-btn">상세정보 보기</button>
              </router-link>
            </div>
          </div>
          <h3 class="director-name">{{ director.name }}</h3>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">🎬</div>
        <p>아직 찜한 감독이 없습니다.</p>
        <router-link to="/movies" class="browse-btn">
          영화 둘러보기
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from '@/components/common/NavBar.vue'
import { useWishStore } from '@/stores/wishlist'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const wishStore = useWishStore()
const { directorWishlist } = storeToRefs(wishStore)

// 로그인 체크 및 데이터 로드
onMounted(async () => {
  if (!userStore.isLoggedIn) {
    router.push({ name: 'login' })
    return
  }
  
  try {
    await wishStore.getDirectorWishlist()
  } catch (error) {
    console.error('Failed to fetch director wishlist:', error)
  }
})

// 정렬 옵션
const sortOptions = ref([
  { id: 1, name: '이름순', type: 'name', active: true }
]);

// 정렬된 감독 목록
const sortedDirectors = computed(() => {
  const activeSort = sortOptions.value.find(opt => opt.active)
  if (!directorWishlist.value) return []
  
  const sorted = [...directorWishlist.value]
  
  switch (activeSort.type) {
    case 'name':
      return sorted.sort((a, b) => a.name.localeCompare(b.name))
    default:
      return sorted
  }
})

// 정렬 옵션 선택
const setSortOption = (option) => {
  sortOptions.value.forEach(opt => {
    opt.active = opt.id === option.id
  })
}

// 찜 취소
const handleWish = async (director) => {
  if (confirm('찜 목록에서 삭제하시겠습니까?')) {
    try {
      await wishStore.wishDirector(director.person_id)
      await wishStore.getDirectorWishlist()  // 목록 갱신
    } catch (err) {
      console.error('Wish error:', err)
    }
  }
}
</script>

<style scoped>
/* 이전 스타일과 동일, 클래스 이름만 변경 */
.wishlist-container {
  min-height: 100vh;
  background-color: #0b001a;
  color: white;
  padding-bottom: 4rem;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header-section {
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #fff;
}

.sort-options {
  display: flex;
  gap: 1rem;
}

.sort-btn {
  padding: 0.5rem 1.5rem;
  background: rgba(131, 70, 255, 0.1);
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 20px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sort-btn:hover {
  background: rgba(131, 70, 255, 0.2);
  transform: translateY(-2px);
}

.sort-btn.active {
  background: #8346ff;
  border-color: #8346ff;
}

.directors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.director-card {
  animation: fadeIn 0.5s ease forwards;
}

.director-poster-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 1/1;  /* 감독 이미지도 정사각형으로 */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.director-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.movie-overlay {
  position: absolute;
  inset: 0;
  background: rgba(11, 0, 26, 0.85);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.5rem;
  opacity: 0;
  transition: all 0.3s ease;
}

.director-poster-wrapper:hover .movie-overlay {
  opacity: 1;
}

.director-poster-wrapper:hover .director-poster {
  transform: scale(1.1);
}

.movie-actions {
  display: flex;
  justify-content: flex-end;
}

.action-btn {
  background: rgba(255, 70, 70, 0.2);
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
  background: rgba(255, 70, 70, 0.4);
  transform: scale(1.1);
}

.detail-btn {
  width: 100%;
  padding: 0.8rem;
  background: #8346ff;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detail-btn:hover {
  background: #9666ff;
}

.director-name {
  margin-top: 1rem;
  text-align: center;
  color: #fff;
  font-size: 1rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 0;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.browse-btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.8rem 2rem;
  background: #8346ff;
  color: white;
  text-decoration: none;
  border-radius: 25px;
  transition: all 0.3s ease;
}

.browse-btn:hover {
  background: #9666ff;
  transform: translateY(-2px);
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
  .content-wrapper {
    padding: 1rem;
  }

  .sort-options {
    justify-content: center;
  }

  .directors-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .director-name {
    font-size: 0.9rem;
  }
}
</style>