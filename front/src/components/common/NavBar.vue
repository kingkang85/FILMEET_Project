<template>
  <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
    <div class="container">
      <!-- Logo -->
      <!-- Logo 부분만 수정 -->
      <RouterLink :to="{name: 'main'}" class="navbar-brand">  
        <svg class="nav-logo" viewBox="0 0 400 80" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style="stop-color:#8346ff;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#a78bfa;stop-opacity:1" />
            </linearGradient>
          </defs>

          <!-- F -->
          <path class="logo-letter" 
                d="M40 20 L40 60 L40 20 L70 20 M40 40 L60 40" 
                stroke="url(#logoGradient)" />
          
          <!-- I -->
          <path class="logo-letter"
                d="M85 20 L85 60 M75 20 L95 20 M75 60 L95 60"
                stroke="url(#logoGradient)" />

          <!-- L -->
          <path class="logo-letter" 
                d="M110 20 L110 60 L140 60" 
                stroke="url(#logoGradient)" />

          <!-- M -->
          <path class="logo-letter" 
                d="M160 60 L160 20 L180 50 L200 20 L200 60" 
                stroke="url(#logoGradient)" />

          <!-- E -->
          <path class="logo-letter" 
                d="M220 20 L220 60 L250 60 M220 20 L250 20 M220 40 L245 40" 
                stroke="url(#logoGradient)" />

          <!-- E -->
          <path class="logo-letter" 
                d="M270 20 L270 60 L300 60 M270 20 L300 20 M270 40 L295 40" 
                stroke="url(#logoGradient)" />

          <!-- T -->
          <path class="logo-letter" 
                d="M320 20 L360 20 M340 20 L340 60" 
                stroke="url(#logoGradient)" />
        </svg>
      </RouterLink>

      <!-- Toggle Button -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarContent"
        aria-controls="navbarContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation Items -->
      <div class="collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink :to="{name: 'main'}" class="nav-link">Home</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{name: 'search'}" class="nav-link">Explore</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{name: 'movielist'}" class="nav-link">Movies</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{name: 'ott'}" class="nav-link">OTT</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{name: 'worldcup'}" class="nav-link">Fun</RouterLink>
          </li>

          <template v-if="isLoggedIn">
            <li class="nav-item">
              <RouterLink :to="{name: 'profile'}" class="nav-link">Profile</RouterLink>
            </li>
            <li class="nav-item">
              <button class="nav-link sign-out-btn" @click="handleLogout">
                Sign out
              </button>
            </li>
          </template>
          <li v-else class="nav-item">
            <RouterLink :to="{name: 'login'}" class="nav-link sign-in-btn">
              Sign in
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div class="nav-spacer"></div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()
const isLoggedIn = computed(() => userStore.isLoggedIn)

const handleLogout = async () => {
  try {
    await userStore.logout()
    alert('로그아웃되었습니다.')
    router.push({ name: 'main' })
  } catch (err) {
    console.error('로그아웃 중 오류 발생:', err)
  }
}
</script>

<style scoped>
.navbar {
  padding: 0.5rem 2rem;
  border-bottom: 1px solid rgba(131, 70, 255, 0.2);
  height: 80px;
  background-color: rgba(11, 0, 26, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 
    0 4px 30px rgba(131, 70, 255, 0.1),
    0 1px 8px rgba(0, 0, 0, 0.2);  
}

.nav-logo {
  height: 45px;
  width: auto;
  filter: drop-shadow(0 0 8px rgba(131, 70, 255, 0.3));
}
rect.logo-letter {
  fill: url(#logoGradient);
  stroke: none;
}
.logo-letter {
  fill: none;
  stroke-width: 8;  /* 더 굵게 */
  stroke-linecap: square;  /* 각진 끝 처리 */
  stroke-linejoin: round;
  transform-origin: center;
  animation: wavyPath 2.5s infinite ease-in-out;
}
.logo-letter:nth-child(2) { animation-delay: 0.0s; }
.logo-letter:nth-child(3) { animation-delay: 0.15s; }
.logo-letter:nth-child(4) { animation-delay: 0.3s; }
.logo-letter:nth-child(5) { animation-delay: 0.45s; }
.logo-letter:nth-child(6) { animation-delay: 0.6s; }
.logo-letter:nth-child(7) { animation-delay: 0.75s; }
.logo-letter:nth-child(8) { animation-delay: 0.9s; }
@keyframes wavyPath {
  0%, 100% {
    transform: translateY(0);
    filter: brightness(1);
  }
  50% {
    transform: translateY(-3px);
    filter: brightness(1.2);
  }
}
.navbar-brand {
  padding: 0;
  display: flex;
  align-items: center;
}

.navbar-brand:hover .nav-logo {
  filter: drop-shadow(0 0 12px rgba(131, 70, 255, 0.5));
}

.nav-link {
  color: #c8c8c8 !important;
  font-family: "Inter", sans-serif;
  font-size: 18px;
  margin: 0 0.8rem;
  padding: 0.5rem 0.3rem;
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
  font-weight: 400;
}

.nav-link::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 0;
  left: 0;
  background-color: #8346ff;
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.nav-link.router-link-active {
  color: #8346ff !important;
  font-weight: 700 !important;
  letter-spacing: 0.3px;
}

.nav-link.router-link-active::after {
  width: 100%;
}

.sign-in-btn, .sign-out-btn {
  /* background: linear-gradient(to right, #8346ff, #9666ff); */
  border-radius: 6px;
  padding: 0.5rem 1.2rem !important;
  margin-left: 2rem !important;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.sign-in-btn:hover, .sign-out-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.sign-in-btn::after, .sign-out-btn::after {
  display: none;
}

.nav-spacer {
  height: 80px;
}

@media (max-width: 992px) {
  .navbar {
    padding: 0.5rem 1rem;
    height: 70px;
  }

  .nav-logo {
    height: 35px;
  }

  .nav-link {
    font-size: 16px;
    margin: 0.5rem 0;
    padding: 0.5rem 1rem !important;
  }

  .navbar-collapse {
    background-color: rgba(11, 0, 26, 0.98);
    margin: 0 -1rem;
    padding: 1rem;
    border-bottom: 1px solid rgba(131, 70, 255, 0.2);
  }

  .sign-in-btn, .sign-out-btn {
    margin: 0.5rem 0 !important;
    padding: 0.5rem 1rem !important;
    background: transparent;
    border-radius: 0;
    text-align: left;
    width: 100%;
  }
}
</style>