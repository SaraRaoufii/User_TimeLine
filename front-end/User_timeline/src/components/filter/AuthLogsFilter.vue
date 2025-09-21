<template>
  <div class="w-full border border-gray-200 rounded-sm shadow-sm bg-gray-50 mb-3 p-2">
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
<div class="flex items-center gap-3 flex-1 min-w-[200px]">
  <v-text-field
    v-model="searchQuery"
    placeholder="Search logs..."
    variant="outlined"
    density="compact"
    clearable
    hide-details="auto"
    append-inner-icon="mdi-magnify"
    class="text-xs text-maincolor placeholder-gray-400 max-w-sm"
    @keyup.enter="applyFilter"
  />
      <button
      @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'; applyFilter()"
      class="flex items-center gap-1 text-xs text-maincolor font-bold px-2 py-1.5 rounded hover:bg-gray-100 transition-colors duration-200 whitespace-nowrap"
    >
      <i class="mdi text-base" :class="sortOrder === 'asc' ? 'mdi-arrow-up' : 'mdi-arrow-down'"></i>
      <span>{{ sortOrder === 'asc' ? 'Oldest First' : 'Newest First' }}</span>
    </button>
  <button
    @click="isOpen = !isOpen"
    class="flex items-center gap-1 text-xs text-maincolor font-bold px-2 py-1.5 rounded hover:bg-gray-100 transition-colors duration-200 whitespace-nowrap"
  >
    <span>{{ isOpen ? 'Hide Filters' : 'Show Filters' }}</span>
    <i class="mdi text-base" :class="isOpen ? 'mdi-chevron-up' : 'mdi-chevron-down'"></i>
  </button>
</div>
    </div>

    <div v-if="isOpen" class="mt-4 pt-4 border-t border-gray-200">
      <div class="font-bold text-maincolor text-sm mb-3 flex items-center">
        <i class="mdi mdi-filter-cog mr-1 text-base"></i>
        Advanced Logs Filters
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <v-select
          v-model="username"
          :items="props.usersList"
          item-title="username"
          item-value="username"
          label="User"
          multiple
          chips
          clearable
          variant="outlined"
          density="compact"
          class="text-xs"
        />

        <v-select
          v-model="action_title"
          :items="actionTypeMap"
          item-title="label"
          item-value="value"
          label="Action"
          multiple
          chips
          clearable
          variant="outlined"
          density="compact"
          class="text-xs"
        />

        <v-text-field
          v-model="start_time"
          type="date"
          label="Start Date"
          variant="outlined"
          density="compact"
          class="text-xs"
        />

        <v-text-field
          v-model="end_time"
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
import { ref } from "vue";
import { Search } from "lucide-vue-next";

const isOpen = ref(false);
const searchQuery = ref(null)
const username = ref([]);
const start_time = ref(null);
const end_time = ref(null);
const action_title = ref([]);
const showDeleteConfirm = ref(false);
const sortOrder = ref("desc") 
const emit = defineEmits(["applyFilter"]);

const props = defineProps({
  usersList: {
    type: Array,
    default: () => [],
  },
});

const actionTypeMap = [
  { label: "Login User", value: "Login user" },
  { label: "Logout User", value: "Logout user" },
  { label: "Login Failed", value: "Login failed" },
  { label: "Account Lock", value: "Account locked" },
];


const applyFilter = () => {
  const formatDate = (dateStr) => (dateStr ? new Date(dateStr).toISOString() : null);

emit("applyFilter", {
    username: username.value.length ? [...username.value] : null,
    start_time: formatDate(start_time.value),
    end_time: formatDate(end_time.value),
    action_title: action_title.value.length ? [...action_title.value] : null,
    search: searchQuery.value && searchQuery.value.trim() !== '' ? searchQuery.value : null,
    sortOrder: sortOrder.value === 'asc' ? 'action_time' : '-action_time'

});

};

const resetFilters = () => {
  username.value = [];
  start_time.value = null;
  end_time.value = null;
  searchQuery.value = null;
  action_title.value = [];

  emit("applyFilter", {
    username: null,
    start_time: null,
    end_time: null,
    action_title: null,
    search: null,
  });
};


</script>
