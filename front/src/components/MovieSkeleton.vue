<!-- components/MovieSkeleton.vue -->
<template>
  <div class="skeleton-card">
    <div class="skeleton-poster"></div>
    <div class="skeleton-title"></div>
  </div>
</template>

<style scoped>
.skeleton-card {
  width: 100%;
  height: 100%;
}

.skeleton-poster {
  width: 100%;
  aspect-ratio: 2/3;
  border-radius: 12px;
  background: linear-gradient(
    90deg,
    rgba(131, 70, 255, 0.05) 25%,
    rgba(131, 70, 255, 0.15) 50%,
    rgba(131, 70, 255, 0.05) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 2s infinite linear;
}

.skeleton-title {
  height: 20px;
  width: 80%;
  margin: 1rem auto 0;
  border-radius: 4px;
  background: linear-gradient(
    90deg,
    rgba(131, 70, 255, 0.05) 25%,
    rgba(131, 70, 255, 0.15) 50%,
    rgba(131, 70, 255, 0.05) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 2s infinite linear;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}
</style>