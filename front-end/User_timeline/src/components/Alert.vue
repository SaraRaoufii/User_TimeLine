<template>
<div 
  v-if="alert.visible"
  :class="[
    'fixed top-5 left-1/2 -translate-x-1/2 z-50 p-4 rounded-lg shadow-lg flex items-center justify-between min-w-[250px] bg-white border-b-4',
    borderClasses[alert.type]
  ]"
>
  <span :class="textClasses[alert.type]">{{ alert.message }}</span>
  <button @click="alert.hide()" class="ml-4 font-bold hover:opacity-80">x</button>
</div>

</template>

<script setup>
import { useAlertStore } from '@/stores/alert'
const alert = useAlertStore()

const borderClasses = {
  info: 'border-maincolor',
  success: 'border-darkgreen',
  warning: 'border-yellow-500',
  error: 'border-darkred'
}

const textClasses = {
  info: 'text-maincolor',
  success: 'text-darkgreen',
  warning: 'text-yellow-500',
  error: 'text-darkred'
}
</script>
