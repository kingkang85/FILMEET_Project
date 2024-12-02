<template>
  <div class="ott-page">
    <NavBar />
    <div class="content-container">
      <OttList />
      <OttRecommendation />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useWishStore } from '@/stores/wishlist'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import NavBar from '@/components/common/NavBar.vue'
import OttList from '@/components/ott/OttList.vue'
import OttRecommendation from '@/components/ott/OttRecommendation.vue'

const wishStore = useWishStore()
const userStore = useUserStore()
const router = useRouter()

onMounted(async () => {
  if (!userStore.isLoggedIn) {
    alert('OTT 추천을 받으려면 로그인이 필요합니다.')
    router.push({ name: 'login' }) 
  } else {
    await wishStore.getMovieWishlist()
  }
})
</script>

<style scoped>
.ott-page {
  background-color: #0b001a;
  min-height: 100vh;
  color: white;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

@media (max-width: 768px) {
  .content-container {
    padding: 1rem;
  }
}
</style>