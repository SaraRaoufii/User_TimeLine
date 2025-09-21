<template>
  <Mainlayout class="flex flex-col gap-5" pagetitle="Dashboard" :items="breadcrumbItems">

  <div class="bg-maincolor text-white p-6 rounded-lg shadow-xl mt-4 flex items-center gap-4">
    <User class="w-8 h-8 text-lightblue" />
    <div>
      <h2 class="text-xl font-bold">Welcome back, {{ currentUsername }}!</h2>
      <p class="mt-1 text-lightblue">Here's a quick overview of your dashboard.</p>
    </div>
  </div>


    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">


      <div class="bg-grayback p-6 rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <h3 class="text-graysecond text-sm font-semibold">Total Users</h3>
          <Users class="w-6 h-6 text-maincolor" />
        </div>
        <p class="text-4xl font-bold text-maincolor mt-2">{{ userCounts.total_users }}</p>
      </div>


      <div class="bg-grayback p-6 rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <h3 class="text-graysecond text-sm font-semibold">Admins</h3>
          <UserCog class="w-6 h-6 text-maincolor" />
        </div>
        <p class="text-4xl font-bold text-maincolor mt-2">{{ userCounts.admin_count }}</p>
      </div>


      <div class="bg-grayback p-6 rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <h3 class="text-graysecond text-sm font-semibold">Active User Today</h3>
          <Activity class="w-6 h-6 text-maincolor" />
        </div>
        <p class="text-4xl font-bold text-maincolor mt-2">{{ activeToday }}</p>
      </div>


      <div class="bg-grayback p-6 rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <h3 class="text-graysecond text-sm font-semibold">Today Logs</h3>
          <FileText class="w-6 h-6 text-maincolor" />
        </div>
        <p class="text-4xl font-bold text-maincolor mt-2">{{ recentLogs }}</p>
      </div>

    </div>
  </Mainlayout>
</template>

<script setup>
import Mainlayout from '@/components/layout/MainLayout.vue';
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { startOfDay, endOfDay } from 'date-fns'

import { UserCog, Users,User, Activity, FileText } from 'lucide-vue-next'

const userStore = useUserStore();
const currentuser= computed(() => userStore);



onMounted(() => {
  userStore.checkLogin()
  currentuser.value = userStore.username || { first_name: 'User' }
})

const USER_COUNTS_QUERY = gql`
  query {
    userCounts {
      totalUsers
      adminCount
    }
  }
`

const ACTIVE_TODAY_QUERY = gql`
query($startTime: DateTime!, $endTime: DateTime!) {
  authLogs(startTime: $startTime, endTime: $endTime, actionTitle: ["Login user"]) {
    user {
      id
    }
  }
}
`

const RECENT_LOGS_QUERY = gql`
query($startTime: DateTime!, $endTime: DateTime!) {
  allLogsCombined(
    page: 1,
    limit: 10000, 
    startTime: $startTime,
    endTime: $endTime
  ) {
    logId
  }
}
`

const userCounts = ref({ total_users: 0, admin_count: 0 })
const activeToday = ref(0)
const recentLogs = ref(0)
const todayStart = startOfDay(new Date())
const todayEnd = endOfDay(new Date()) 

const { onResult: onUserCountsResult } = useQuery(USER_COUNTS_QUERY)
onUserCountsResult((res) => {
  if (res.data && res.data.userCounts) {
    userCounts.value = {
      total_users: res.data.userCounts.totalUsers,
      admin_count: res.data.userCounts.adminCount
    }
  }
})

const { result: activeResult } = useQuery(ACTIVE_TODAY_QUERY, {
  startTime: todayStart.toISOString(),
  endTime: todayEnd.toISOString()
})

const { result: recentLogsResult } = useQuery(RECENT_LOGS_QUERY, {
  startTime: todayStart.toISOString(),
  endTime: todayEnd.toISOString()
})

watch(recentLogsResult, (res) => {
  if (res?.allLogsCombined) {
    recentLogs.value = res.allLogsCombined.length
  }
})

watch(activeResult, (res) => {
  if (res?.authLogs) {
    const uniqueUsers = new Set(res.authLogs.map(log => log.user.id))
    activeToday.value = uniqueUsers.size
  }
})

const breadcrumbItems = computed(() => [
  { title: 'Home', href: '/' },
])
</script>
