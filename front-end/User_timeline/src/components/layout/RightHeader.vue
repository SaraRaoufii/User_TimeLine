<template>
  <div class="flex flex-col md:flex-row md:gap-6 items-center md:justify-between">   
    <div class="userscount flex flex-row gap-1 text-maincolor w-full justify-center md:justify-start  md:order-3">
      <UserStateHead :icon="Users" :count="totalUsers" title="Users" />
      <UserStateHead :icon="UserCog" :count="adminCount" title="Admins" />
    </div>

  <v-btn
    size="small"
    class="bg-maincolor text-inactive rounded-lg flex items-center gap-1 px-3 pt-0 min-h-[30px] md:min-h-[36px] shadow-sm hover:bg-maincolor/90 normal-case min-w-[8px] md:w-auto mt-0 md:mt-0 justify-center md:order-1 text-[11px] md:text-[14px]"
  >
    <Plus class="stroke-[1.5] w-[14px] h-[14px] md:w-[18px] md:h-[18px]" />
    Add User
  </v-btn>


  </div>
</template>

<script setup>
import { UserCog, Users, Plus } from 'lucide-vue-next';
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { computed } from 'vue'
import UserStateHead from '@/components/layout/UserStateHead.vue'

const GET_userCounts = gql`
  query {
    userCounts {
      totalUsers
      adminCount
    }
  }
`

const { result} = useQuery(GET_userCounts)

const totalUsers = computed(() => result.value?.userCounts?.totalUsers || 0)
const adminCount = computed(() => result.value?.userCounts?.adminCount || 0)
</script>
