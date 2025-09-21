<script setup>
import Mainlayout from '@/components/layout/MainLayout.vue'
import LogList from '@/components/activity/LogList.vue'
import TimelineComponent from '@/components/activity/TimelineComponent.vue'
import UserInfo from '@/components/users/UserInfo.vue'
import EditUser from '@/components/users/EditUser.vue'
import { ref, computed, watch } from 'vue'
import { UserRound, Activity } from 'lucide-vue-next'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { useUserStore } from '@/stores/user'
import { useRoute } from 'vue-router'

const route = useRoute()
const username = route.params.username
const userStore = useUserStore()
const isOwnProfile = computed(() => username === userStore.currentUser.username)
const profileUser = ref({})
const isEditing = ref(false)
const tab = ref('tab-1')


const breadcrumbItems = computed(() => [
  { title: 'Home', href: '/' },
  { title: 'Users list', href: '/userslistpage' },
  { title: profileUser.value.username || '', href: `/userslistpage/profile/${profileUser.value.username}` }
])


const GET_USER_BY_USERNAME = gql`
  query getUserByUsername($username: String!) {
    userByUsername(username: $username) {
      username
      email
      address
      phone
      role
      firstName
      lastName
      id
      isActive
      password
      isLocked
      failedLoginAttempts
    }
  }
`

const loading = ref(false)
const error = ref(null)
const safeError = ref(null)

if (!isOwnProfile.value) {
  const { result, loading: l, error: e } = useQuery(GET_USER_BY_USERNAME, { username })
  watch(l, (val) => (loading.value = val))
    watch(e, (val) => {
    if (val) {
      console.error('Apollo error:', val) 
      safeError.value = 'Failed to load user info. Please try again later.'
    }
  })
  watch(result, (val) => {
    profileUser.value = val?.userByUsername || {}
  })
} else {
  profileUser.value = userStore.currentUser
}

const handleSave = (updatedUser) => {
  isEditing.value = false
  profileUser.value = updatedUser
}


watch(
  () => route.query.edit,
  (val) => {
    isEditing.value = val === 'true'
  },
  { immediate: true }
)
</script>

<template>
  <Mainlayout 
    class="allpannel flex flex-row gap-5" 
    pagetitle="User Panel" 
    :items="breadcrumbItems" 
    :loading="loading" 
    :error="error"
  >
    <div class="tabs w-full mt-6 ml-1">

      <div class="styletab flex gap-4 bg-white border-b border-grayback overflow-x-auto">
        <button
          @click="tab = 'tab-1'"
          :class="[
            'v-tab relative flex items-center gap-2 px-4 py-2 text-base font-semibold transition-all duration-300 ease-in-out',
            tab === 'tab-1' ? 'text-white bg-maincolor rounded-t-lg shadow-sm' : 'text-graysecond hover:text-maincolor hover:bg-grayback'
          ]"
        >
          <UserRound class="w-5 h-5 stroke-[1.8]" />
          User Information
          <span v-if="tab==='tab-1'" class="absolute -bottom-1 left-0 w-full h-1 bg-maincolor rounded-t"></span>
        </button>

        <button
          @click="tab = 'tab-2'"
          :class="[
            'v-tab relative flex items-center gap-2 px-4 py-2 text-base font-semibold transition-all duration-300 ease-in-out',
            tab === 'tab-2' ? 'text-white bg-maincolor rounded-t-lg shadow-sm' : 'text-graysecond hover:text-maincolor hover:bg-grayback'
          ]"
        >
          <Activity class="w-5 h-5 stroke-[1.8]" />
          Activity Logs
          <span v-if="tab==='tab-2'" class="absolute -bottom-1 left-0 w-full h-1 bg-maincolor rounded-t"></span>
        </button>
      </div>

      <div class="v-tabs-window mt-5">
        <div v-show="tab === 'tab-1'" class="v-tabs-window-item">
          <UserInfo
            v-if="!isEditing && profileUser.username"
            v-bind="profileUser"
            @edit="isEditing = true" 
          />

          <EditUser
            v-else-if="isEditing && profileUser.username"
            v-bind="profileUser"
            @cancel="isEditing = false"
            @saved="handleSave"
          />
        </div>

        <div v-show="tab === 'tab-2'" class="v-tabs-window-item">
          <LogList :username="username">
          <template #default="{ logs, loading, isLastPage, handleScroll }">
              <TimelineComponent 
                :filteredTimeline="logs" 
                :loading="loading" 
                :isLastPage="isLastPage" 
                @scroll="handleScroll"
              />

          </template>
        </LogList>
        </div>
      </div>
    </div>
  </Mainlayout>
</template>
