<template>
  <div class="count flex flex-col rounded-lg px-1 py-1 md:mt-1 md:min-w-[70px] items-center md:shadow-sm md:bg-grayback">
    <div class="flex flex-row gap-1 items-center">
      <component :is="icon" class="w-4 h-4 md:w-5 md:h-5 stroke-[1.3]" />
      <div class="num text-[12px] md:text-[14px] font-semibold">{{ count }}</div>
    </div>
    <div class="user text-[11px] md:text-[13px] text-graysecond">
      {{ title }}
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  icon: Object, 
  count: Number,
  title: String
});
</script>