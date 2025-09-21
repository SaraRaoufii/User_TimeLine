<template>
  <div class="w-full border border-gray-200 rounded-sm shadow-sm bg-gray-50 mb-2 p-2 mt-2">
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
<div class="flex items-center gap-3 flex-1 min-w-[200px]">
  <v-text-field
    v-model="searchQuery"
    placeholder="Search users..."
    variant="outlined"
    density="compact"
    clearable
    hide-details="auto"
    append-inner-icon="mdi-magnify"
    class="text-xs text-maincolor placeholder-gray-400 max-w-sm"
    @keyup.enter="applyFilter"
  />
  <button
    @click="isOpen = !isOpen"
    class="flex items-center gap-1 text-xs text-maincolor font-bold px-2 py-1.5 rounded hover:bg-gray-100 transition-colors duration-200 whitespace-nowrap"
  >
    <span>{{ isOpen ? 'Hide Filters' : 'Show Filters' }}</span>
    <i class="mdi text-base" :class="isOpen ? 'mdi-chevron-up' : 'mdi-chevron-down'"></i>
  </button>
</div>

<v-btn
  @click="downloadCSV"
  icon
  size="small" 
  class="bg-gray-50"
>
  <Download class="w-5 h-5 stroke-[1.7] text-darkgreen" />
</v-btn>


    </div>


    <div v-if="isOpen" class="mt-4 pt-4 border-t border-gray-200">
      <div class="font-bold text-maincolor text-sm mb-3 flex items-center">
        <i class="mdi mdi-filter-cog mr-1 text-base"></i>
        Advanced Users Filters
      </div>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <v-select
            v-model="is_active"
            :items="['All' , 'Active' , 'InActive']"
            label="Active Status"
            clearable
            variant="outlined"
            density="compact"
            class="text-xs"
            />
            <v-text-field
            v-model="login_num"
            label="Login Number"
            variant="outlined"
            density="compact"
            class="text-xs"
            />         
            <v-text-field
            v-model="startDate"
            type="date"
            label="Start Date"
            variant="outlined"
            density="compact"
            class="text-xs"
            />

            <v-text-field
            v-model="endDate"
            type="date"
            label="End Date"
            variant="outlined"
            density="compact"
            class="text-xs"
            />
        </div>

      <div class="flex justify-end gap-2 mt-1">
        <v-btn
          @click="resetFilters"
          size="small"
          class="bg-gray-100 text-maincolor hover:bg-gray-200 text-xs normal-case px-3 py-1 rounded-lg shadow-sm"
        >
          Clear
        </v-btn>

        <v-btn
          @click="applyFilter"
          size="small"
          class="bg-maincolor text-white hover:bg-maincolor text-xs normal-case px-3 py-1 flex items-center rounded-lg shadow-sm"
        >
          <i class="mdi mdi-magnify mr-1 text-sm"></i>
          Apply
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue"
import { Search } from 'lucide-vue-next'
import { Download } from 'lucide-vue-next'
import {useAlertStore} from '@/stores/alert'

const isOpen = ref(false)
const searchQuery = ref(null)
const is_active=ref(null)
const login_num=ref(null)
const startDate = ref(null)
const endDate = ref(null)
const props = defineProps({
  users: { type: Array, default: () => [] } 
})

const alert= useAlertStore()


const emit = defineEmits(['applyFilter'])

const applyFilter = () => {
    let activeValue = null
    if (is_active.value === 'Active') activeValue = true
    else if (is_active.value === 'InActive') activeValue = false


    emit('applyFilter', {
        is_active: activeValue === null ? null : activeValue,
        login_num: login_num.value ? Number(login_num.value) : null,
        start_date: startDate.value || null,
        end_date: endDate.value || null,
        search: searchQuery.value && searchQuery.value.trim() !== '' ? searchQuery.value : null,
    })
}

const resetFilters = () => {
  is_active.value = null
  login_num.value = null
  startDate.value = null
  endDate.value = null
  searchQuery.value = null

  emit("applyFilter", {
    is_active: null,
    login_num: null,
    start_date: null,
    end_date: null,
    search: null,
  });
};

const downloadCSV = () => {
  if (!props.users || props.users.length === 0) {
    alert.show("No users to export", 'warning')
    return
  }

  const headers = ["Username","role", "First Name", "Last Name", "Email", "Status", "Locked" ]
  let csvContent = headers.join(",") + "\n"

    props.users.forEach(u => {
    const row = [
      `"${u.username || ""}"`,
      `"${u.role || ""}"`,
      `"${u.firstName || ""}"`,
      `"${u.lastName || ""}"`,
      `"${u.email || ""}"`,
      `"${u.isActive ? "Active" : "Inactive"}"`,
      `"${u.isLocked ? "Locked" : "Unlocked"}"`
    ]
    csvContent += row.join(",") + "\n"
  })

  const BOM = "\uFEFF"
  const blob = new Blob([BOM + csvContent], { type: "text/csv;charset=utf-8;" })
  const link = document.createElement("a")
  link.href = URL.createObjectURL(blob)
  link.setAttribute("download", "users.csv")
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
  
</script>