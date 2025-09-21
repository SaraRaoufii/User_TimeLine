<template>
  <Mainlayout class="allpannel flex flex-row gap-5" pagetitle="Create User" :items="breadcrumbItems" >
    <div class="list w-full">
      <CreateUser />
    </div>
  </Mainlayout>
</template>

<script setup>
import CreateUser from '@/components/users/CreateUser.vue';
import Mainlayout from '@/components/layout/MainLayout.vue';
import {computed} from 'vue'

  const breadcrumbItems = computed(() => [
    { title: 'Home', href: '/' },
  ])
   

</script>

