<!-- src/components/ChatMessage.vue -->
<template>
  <div :class="['message', type]">
    <div class="message-content">{{ content }}</div>
    <div v-if="type === 'ai'" class="message-time">{{ time }}</div>
  </div>
</template>

<script setup>
defineProps({
  content: {
    type: String,
    required: true
  },
  type: {
    type: String,
    required: true
  },
  time: String
})
</script>

<style scoped>
.message {
  max-width: 80%;
  padding: 0.75rem;
  border-radius: 0.5rem;
  animation: messageSlide 0.3s ease;
}

.message.user {
  background: rgba(131, 70, 255, 0.2);
  color: white;
  margin-left: auto;
}

.message.ai {
  background: rgba(255, 255, 255, 0.05);
  color: #ddd;
}

.message.system {
  background: rgba(255, 193, 7, 0.2);
  color: #ffe082;
  font-size: 0.875rem;
  font-style: italic;
  margin: 0 auto;
  max-width: 90%;
  text-align: center;
}

.message-content {
  line-height: 1.5;
}

.message-time {
  font-size: 0.75rem;
  color: #888;
  margin-top: 0.25rem;
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>