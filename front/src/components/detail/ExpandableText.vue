<template>
  <div class="expandable-text">
    <p :class="textClass">
      {{ displayText }}
    </p>
    
    <button
      v-if="shouldTruncate"
      @click="toggleExpand"
      class="expand-button"
    >
      {{ isExpanded ? '접기' : '더보기' }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  text: {
    type: String,
    required: true,
    default: ''  // text prop의 기본값 추가
  },
  maxLength: {
    type: Number,
    default: 300
  },
  class: {
    type: String,
    default: ''
  }
});

const isExpanded = ref(false);

const shouldTruncate = computed(() => {
  // text가 undefined나 null일 경우를 처리
  return props.text && props.text.length > props.maxLength;
});

const displayText = computed(() => {
  if (!props.text) return '';  // text가 없을 경우 빈 문자열 반환
  if (!shouldTruncate.value || isExpanded.value) {
    return props.text;
  }
  return props.text.slice(0, props.maxLength) + '...';
});

const textClass = computed(() => [
  props.class,
  { 'expanded': isExpanded.value }
]);

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value;
};
</script>

<style scoped>
.expandable-text {
  position: relative;
}

.expand-button {
  display: inline-block;
  color: #a78bfa;
  background: none;
  border: none;
  padding: 0.5rem 0;
  margin-top: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.expand-button:hover {
  color: #8346ff;
}

.expanded {
  max-height: none;
}
</style>