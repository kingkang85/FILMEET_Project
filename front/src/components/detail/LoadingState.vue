// LoadingState.vue
<template>
  <div class="loading-state">
    <div class="loading-content">
      <div class="loading-skeleton">
        <div class="skeleton-image"></div>
        <div class="skeleton-info">
          <div class="skeleton-line large"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line small"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loading-state {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.loading-skeleton {
  display: flex;
  gap: 2rem;
}

.skeleton-image {
  width: 300px;
  height: 450px;
  background: linear-gradient(
    90deg,
    rgba(131, 70, 255, 0.1) 25%,
    rgba(131, 70, 255, 0.2) 50%,
    rgba(131, 70, 255, 0.1) 75%
  );
  background-size: 200% 100%;
  border-radius: 12px;
  animation: shimmer 2s infinite;
}

.skeleton-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.skeleton-line {
  height: 20px;
  background: linear-gradient(
    90deg,
    rgba(131, 70, 255, 0.1) 25%,
    rgba(131, 70, 255, 0.2) 50%,
    rgba(131, 70, 255, 0.1) 75%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  animation: shimmer 2s infinite;
}

.skeleton-line.large {
  height: 40px;
  width: 80%;
}

.skeleton-line.small {
  width: 60%;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (max-width: 768px) {
  .loading-skeleton {
    flex-direction: column;
  }

  .skeleton-image {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
  }
}
</style>
