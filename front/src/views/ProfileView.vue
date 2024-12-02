<template>
  <div class="mypage-container" v-if="user">
    <NavBar />
    
    <ProfileHeader 
      :user="user" 
      @openModal="showEditModal = true" 
      @openPasswordModal="showPasswordModal = true"
    />

    <div class="divider"></div>

    <div class="content-section">
      <!-- 찜한 영화 -->
      <WishlistSection
        :user="user"
        title="찜한 목록"
        :items="movieWishlistPreview"
        routeName="wishmovies"
        detailRouteName="moviedetail"
        idKey="movie_id"
        imageKey="poster_path"
        nameKey="title"
      />

      <div class="divider"></div>

      <!-- 찜한 배우 -->
      <WishlistSection
        :user="user"
        title="찜한 배우"
        :items="actorWishlistPreview"
        routeName="wishactors"
        detailRouteName="actordetail"
        idKey="person_id"
        imageKey="profile_path"
        nameKey="name"
      />

      <div class="divider"></div>

      <!-- 찜한 감독 -->
      <WishlistSection
        :user="user"
        title="찜한 감독"
        :items="directorWishlistPreview"
        routeName="wishdirectors"
        detailRouteName="directordetail"
        idKey="person_id"
        imageKey="profile_path"
        nameKey="name"
      />
    </div>

    <EditProfileModal
      :show="showEditModal"
      :initialData="user"
      @close="showEditModal = false"
      @update="handleProfileUpdate"
    />

    <ChangePasswordModal
      :show="showPasswordModal"
      @close="showPasswordModal = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavBar from '@/components/common/NavBar.vue'
import ProfileHeader from '@/components/profile/ProfileHeader.vue'
import WishlistSection from '@/components/profile/WishlistSection.vue'
import EditProfileModal from '@/components/profile/EditProfileModal.vue'
import ChangePasswordModal from '@/components/profile/ChangePasswordModal.vue'
import { useUserStore } from '@/stores/user'
import { useWishStore } from '@/stores/wishlist'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { computed, onMounted } from 'vue'

const router = useRouter()
const userStore = useUserStore()
const wishStore = useWishStore()
const showEditModal = ref(false)
const showPasswordModal = ref(false)

const { user } = storeToRefs(userStore)
const { movieWishlist, actorWishlist, directorWishlist } = storeToRefs(wishStore)

const movieWishlistPreview = computed(() => movieWishlist.value?.slice(0, 5) || [])
const actorWishlistPreview = computed(() => actorWishlist.value?.slice(0, 5) || [])
const directorWishlistPreview = computed(() => directorWishlist.value?.slice(0, 5) || [])

const handleProfileUpdate = () => {
  userStore.getUserInfo()
}

onMounted(() => {
  if (userStore.isLoggedIn) {
    wishStore.getMovieWishlist()
    wishStore.getActorWishlist()
    wishStore.getDirectorWishlist()
  } else {
    router.push({ name: 'login' })
  }
})
</script>

<style scoped>
.mypage-container {
  min-height: 100vh;
  background-color: #0b001a;
  color: white;
  padding-bottom: 4rem;
}

.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.divider {
  max-width: 1200px;
  margin: 2rem auto;
  height: 1px;
  background: linear-gradient(
    to right,
    transparent,
    #8346ff,
    transparent
  );
  opacity: 0.3;
}

@media (max-width: 768px) {
  .content-section {
    padding: 0 1rem;
  }

  .divider {
    margin: 1.5rem auto;
  }
}
</style>