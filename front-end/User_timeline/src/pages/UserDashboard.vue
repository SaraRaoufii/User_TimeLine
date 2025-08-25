<template>
    <Mainlayout class="flex flex-row gap-5" pagetitle="Dashboard" :items="breadcrumbItems">

    </Mainlayout>
    

</template>

<script setup>
import Mainlayout from '@/components/layout/MainLayout.vue';
import {computed, onMounted } from 'vue'
import { useUserStore} from '@/stores/user'


  const userStore = useUserStore()

  onMounted(() => {
  userStore.checkLogin()
})

  const breadcrumbItems = computed(() => [
    { title: 'Home', href: '/' },
  ])
</script>

