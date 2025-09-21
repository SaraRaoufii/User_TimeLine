<template>
  <Mainlayout class="allpannel flex flex-row gap-5" pagetitle="Users List" :items="breadcrumbItems" >
    <div class="list w-full">
      <UsersList />
    </div>
  </Mainlayout>
</template>

<script setup>
import UsersList from '@/components/users/UsersList.vue';
import Mainlayout from '@/components/layout/MainLayout.vue';
import {computed} from 'vue'
import { onBeforeUnmount, onDeactivated } from 'vue'
  const breadcrumbItems = computed(() => [
    { title: 'Home', href: '/' },
    { title: 'Users list', href: '/userslistpage' },
  ])

 onBeforeUnmount(() => {
  document.querySelectorAll('.v-overlay-container, .v-tooltip').forEach(el => el.remove())
})
onDeactivated(() => {
  document.querySelectorAll('.v-overlay-container, .v-tooltip').forEach(el => el.remove())
})      

</script>

