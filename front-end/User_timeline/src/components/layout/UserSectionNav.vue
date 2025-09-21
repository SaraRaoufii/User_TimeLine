<template>
  <div class="sidebar-user">
    <div v-show="isCollapsed && !isMobile" class="user-circle flex justify-center m-3">
      <div class="user-initial w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm bg-lightblue text-maincolor shadow-md">
        {{ userInitial }}
      </div>
    </div>
    <div
      v-show="!isCollapsed || isMobile"
      class="user-info flex items-center p-3 m-3 rounded-xl bg-lightblue text-maincolor hover:bg-lightblue/90 cursor-pointer shadow hover:shadow-md transition-all duration-300"
    >
      <div class="user-initial-full w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm bg-white text-maincolor">
        {{ userInitial }}
      </div>
      <div class="user-details ml-3 overflow-hidden">
        <div class="username font-semibold text-xs truncate hover:underline" @click="goToUser(userStore.currentUser.username)"> 
          {{ userStore.currentUser.username }}
        </div>
        <p class="role text-[11px] truncate text-graysecond/80">
          {{ userStore.currentUser.role }}
        </p>
      </div>
      <div class="pl-11">
          <LogOut class="w-6 h-6 text-maincolor" @click="handleLogout" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router'
import { LogOut, UserStar } from 'lucide-vue-next'
import { useAlertStore} from '@/stores/alert'

const alertStore = useAlertStore()
const userStore = useUserStore();
const router = useRouter()
const props = defineProps({
  isCollapsed: Boolean,
  isMobile: {
    type: Boolean,
    default: false,
  },
});

const userInitial = computed(() =>
  userStore.currentUser?.username?.charAt(0).toUpperCase() || ''
);
 const goToUser = (username) => {
  router.push(`/userpanel/${username}`)
}
const handleLogout = ()=>{
  userStore.logout()
  router.push('/login')
  alertStore.show('Youhave been loged out' , 'success')
}
</script>