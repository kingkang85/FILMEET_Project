<template>
  <div class="section-header">
    <h2 class="section-title">{{ title }}</h2>
    <slot name="actions"></slot>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.section-header {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
}

.section-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(
    to right,
    transparent,
    rgba(131, 70, 255, 0.3),
    transparent
  );
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  background: linear-gradient(to right, #ffffff, #a78bfa);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.75rem;
  }
}
</style>