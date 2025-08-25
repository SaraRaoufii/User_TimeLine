import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUIStore = defineStore('ui', () => {
  const sidebarCollapsed = ref(true); 

  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value;
    localStorage.setItem('sidebarCollapsed', sidebarCollapsed.value); 
  };

  if (localStorage.getItem('sidebarCollapsed') !== null) {
    sidebarCollapsed.value = localStorage.getItem('sidebarCollapsed') === 'true';
  }

  return { sidebarCollapsed, toggleSidebar };
});
