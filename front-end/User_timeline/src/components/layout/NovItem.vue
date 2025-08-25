<template>
  <li class="w-full">
    <router-link
      :to="item.path"
      @click="handleCloseMenu"
      :class="linkClasses"
    >
      <component :is="item.icon" class="w-5 h-5 flex-shrink-0" />
      <span :class="textClasses">{{ item.name }}</span>
    </router-link>
  </li>
</template>

<script setup>
import { computed } from 'vue';
import { useUIStore } from '@/stores/ui';

const uiStore = useUIStore();

const props = defineProps({
  item: Object,
  isCollapsed: Boolean,
  isMobile: Boolean,
});

const emit = defineEmits(['close-menu']);

const linkClasses = computed(() => [
  'flex items-center gap-3 py-2 px-3 rounded-lg transition-all duration-300 ease-in-out relative',
  props.item.isActive
    ? 'bg-lightblue text-maincolor font-semibold shadow-md'
    : props.isMobile
    ? 'text-graysecond hover:bg-lightblue/30 hover:text-maincolor'
    : props.isCollapsed
    ? 'text-graysecond hover:bg-grayback hover:text-maincolor hover:scale-105'
    : 'text-graysecond hover:bg-gradient-to-r hover:from-lightblue/20 hover:to-lightblue/50 hover:text-maincolor hover:scale-105',
]);

const textClasses = computed(() => [
  'text-sm font-medium whitespace-nowrap transition-all duration-300 ease-in-out',
  props.isMobile || !props.isCollapsed
    ? 'opacity-100 w-auto'
    : 'opacity-0 w-0 overflow-hidden',
  props.item.isActive ? 'font-semibold' : '',
]);

const handleCloseMenu = () => {
  if (props.isMobile) {
    emit('close-menu');
  }
};
</script>