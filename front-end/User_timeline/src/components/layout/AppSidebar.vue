<template>
  <div class="relative flex">

    <aside
      :class="[ 
        'hidden md:flex flex-col z-50 justify-between transition-all duration-300 shadow-lg rounded-lg overflow-hidden',
        uiStore.sidebarCollapsed
          ? 'sidebar-collapsed w-16 m-2 bg-white text-maincolor'
          : 'sidebar-expanded w-56 m-4 mr-2 bg-maincolor text-white'
      ]"
    >
      <div class="title flex flex-col items-center justify-center p-4">
        <h2
          class="text-lg font-bold relative transition-opacity duration-300"
          :class="uiStore.sidebarCollapsed ? 'opacity-0' : 'opacity-100'"
        >
          User Timeline
          <span
            v-if="!uiStore.sidebarCollapsed"
            class="absolute -bottom-1 left-0 w-full h-0.5 bg-lightblue rounded transition-all duration-300"
          ></span>
        </h2>
      </div>

      <nav class="desktop-nav flex-grow px-2 mt-4">
        <ul class="space-y-3">
          <NavItem
            v-for="item in navItems"
            :key="item.path"
            :item="item"
            :is-collapsed="uiStore.sidebarCollapsed"
          />
        </ul>
      </nav>

      <UserSectionNav :is-collapsed="uiStore.sidebarCollapsed" />
    </aside>

    
    <transition name="slide">
      <aside
          v-if="mobileMenuOpen"
          class="fixed inset-y-0 left-0 w-56 bg-maincolor text-white shadow-lg z-50 flex flex-col justify-between rounded-r-lg p-4 md:hidden"
        >
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-lg font-bold">User Timeline</h2>
            <button
              @click="$emit('update:mobileMenuOpen', false)"
              class="w-9 h-9 flex items-center justify-center
                    bg-lightblue text-maincolor rounded-full shadow hover:scale-105 transition"
            >
              <X class="h-5 w-5" />
            </button>

          </div>

       
          <nav class="mobile-nav flex-grow">
            <ul class="space-y-3">
              <NavItem
                v-for="item in navItems"
                :key="item.path"
                :item="item"
                is-mobile
                :is-collapsed="uiStore.sidebarCollapsed"
                @close-menu="$emit('update:mobileMenuOpen', false)"
              />
            </ul>
          </nav>

        <UserSectionNav :is-collapsed="uiStore.sidebarCollapsed" is-mobile />    
      </aside>
    </transition>

    <div 
      v-if="mobileMenuOpen" 
      @click="mobileMenuOpen = false" 
      class="fixed inset-0 bg-black/40 z-40 md:hidden"
    ></div>

    <button
      @click="toggleSidebar"
      :class="[ 
        'sidebar-toggle absolute top-1/2 -translate-y-1/2 p-2 rounded-full shadow-md transition-all duration-300 z-50 hover:scale-110 hidden md:block',
        uiStore.sidebarCollapsed ? 'toggle-collapsed left-[3.5rem] bg-lightblue text-maincolor z-100' : 'toggle-expanded left-[13.5rem] bg-maincolor text-white z-50'
      ]"
    >
      <ChevronLeft v-if="!uiStore.sidebarCollapsed" class="w-5 h-5" />
      <ChevronRight v-else class="w-5 h-5" />
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { LayoutDashboard, UsersRound, Fingerprint, IdCard, ChevronLeft, ChevronRight,X } from 'lucide-vue-next';
import { useUserStore } from '@/stores/user';
import { useUIStore } from '@/stores/ui';
import NavItem from '@/components/layout/NovItem.vue'
import UserSectionNav from '@/components/layout/UserSectionNav.vue';

const uiStore = useUIStore();
const route = useRoute();
const userStore = useUserStore();

const props = defineProps({
  mobileMenuOpen: Boolean
});


const userInitial = computed(() =>
  userStore.currentUser?.username?.charAt(0).toUpperCase() || ''
);

const navItems = computed(() => [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard, isActive: route.path === '/' },
  { name: 'Users List', path: '/userslistpage', icon: UsersRound, isActive: route.path.startsWith('/userslistpage') },
  { name: 'Management Logs', path: '/managelogs', icon: IdCard, isActive: route.path === '/managelogs' },
  { name: 'Authentication Logs', path: '/authlogs', icon: Fingerprint, isActive: route.path === '/authlogs' }
]);

const toggleSidebar = () => {
  uiStore.sidebarCollapsed = !uiStore.sidebarCollapsed;
};
</script>
