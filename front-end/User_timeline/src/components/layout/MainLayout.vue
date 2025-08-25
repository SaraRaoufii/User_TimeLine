<template>
  <div class="flex flex-col md:flex-row h-screen overflow-hidden text-gray-800">
    <Sidebar
      v-model:mobileMenuOpen="mobileMenuOpen"
      :user="userStore.currentUser"
    />

    <div class="main-area flex-grow flex flex-col w-full pr-2 md:pr-4 relative">

      <header class="page-header sticky top-0 z-20 bg-white flex flex-col mt-1 mb-0 min-h-[50px] md:min-h-[60px]">
        <div class="flex items-center justify-between mb-0.5">
          <div class="flex items-center">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="md:hidden ml-0 w-9 h-9 rounded-full flex items-center justify-center
                     bg-lightblue text-maincolor shadow hover:scale-105 transition"
            >
              <Menu v-if="!mobileMenuOpen" class="h-5 w-5" />
              <X v-else class="h-5 w-5" />
            </button>
            <h1 class="ml-2 page-title text-base sm:text-xl md:text-2xl font-bold text-maincolor truncate">
              {{ pagetitle }}
            </h1>
          </div>

          <div class="right-header ml-2">
            <RightHeader />
          </div>
        </div>

        <v-breadcrumbs
          v-if="items.length"
          :items="items"
          class="hidden sm:flex p-0 text-xs text-graysecond gap-1 w-auto mb-1"
        >
          <template v-slot:item="{ item }">
            {{ item.title.toUpperCase() }}
          </template>
        </v-breadcrumbs>
      </header>

      <div class="border-t border-maincolor/30 w-full"></div>

      <main class="main-content flex-grow overflow-y-auto">
        <div v-if="loading" class="flex justify-center items-center h-full">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>
        <div v-else-if="error" class="flex justify-center items-center h-full text-darkred">
          <p>An error occurred: {{ error.message }}</p>
        </div>
        <slot v-else />
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from "@/components/layout/AppSidebar.vue";
import RightHeader from "@/components/layout/RightHeader.vue";
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';
import { Menu, X } from 'lucide-vue-next';

defineProps({
  pagetitle: { type: String, default: "" },
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: Object, default: null },
});

const userStore = useUserStore();
const mobileMenuOpen = ref(false);
</script>
