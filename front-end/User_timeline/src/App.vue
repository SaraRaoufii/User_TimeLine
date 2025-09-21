<script setup>
import {  RouterView, useRouter } from 'vue-router'
import Alert from './components/Alert.vue';
import { useApolloClient } from '@vue/apollo-composable'

const router = useRouter()
const apolloClient = useApolloClient().client

router.afterEach(() => {
  apolloClient.resetStore()
})
</script>

<template>
  <div class="app-root">
    <router-view v-slot="{ Component, route }">
      <keep-alive>
        <component :is="Component" :key="route.fullPath" />
      </keep-alive>
    </router-view>
    <Alert />
  </div>
</template>



<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700;800&display=swap');

body {
 font-family: "Open Sans", sans-serif;
 margin: 0;
 padding: 0;
}

html, body {
  margin: 0;
  padding: 0;
}


</style>