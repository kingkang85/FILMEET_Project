<template>
  <div class="action-buttons">
    <button 
      v-for="(button, index) in buttons" 
      :key="index"
      :class="['action-btn', button.class]"
      @click="button.onClick"
    >
      <span class="action-icon">{{ button.icon }}</span>
      <span v-if="button.label" class="action-label">{{ button.label }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  buttons: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.action-buttons {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: none;
  border-radius: 50%;
  background: rgba(131, 70, 255, 0.1);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(131, 70, 255, 0.2);
  transform: scale(1.1);
}

.action-icon {
  font-size: 1.5rem;
}

.action-label {
  font-size: 0.9rem;
  display: none;
}

.action-btn.with-label {
  border-radius: 25px;
  padding: 0.75rem 1.25rem;
}

.action-btn.with-label .action-label {
  display: block;
}

@media (max-width: 640px) {
  .action-buttons {
    justify-content: center;
  }
}
</style>