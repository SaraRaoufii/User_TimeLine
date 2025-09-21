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

      <v-btn
        @click="confirmDeleteAllLogs"
        size="small"
        class="border-[1.5] border-darkred text-darkred hover:bg-red-700 hover:text-white text-xs normal-case px-2 py-1 flex items-center rounded-lg shadow-sm"
      >
        <i class="mdi mdi-delete-forever mr-1 text-sm"></i>
        Delete All Logs
      </v-btn>
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
        
        <div class="grid grid-cols-2 gap-2">
          <v-select
            v-model="old_key"
            :items="valueFields"
            item-title="label"
            item-value="value"
            label="Old Field"
            clearable
            variant="outlined"
            density="compact"
            class="text-xs"
          />
          <v-text-field
            v-model="old_val"
            label="Old Value"
            variant="outlined"
            density="compact"
            class="text-xs"
          />
        </div>

        <div class="grid grid-cols-2 gap-2">
          <v-select
            v-model="new_key"
            :items="valueFields"
            item-title="label"
            item-value="value"
            label="New Field"
            clearable
            variant="outlined"
            density="compact"
            class="text-xs"
          />
          <v-text-field
            v-model="new_val"
            label="New Value"
            variant="outlined"
            density="compact"
            class="text-xs"
          />
        </div>

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
          class="bg-gray-100 text-gray-600 hover:bg-gray-200 text-xs normal-case px-3 py-1 rounded-lg shadow-sm"
        >
          Clear
        </v-btn>
        <v-btn
          @click="applyFilter"
          size="small"
          class="bg-maincolor text-white hover:bg-maincolor/90 text-xs normal-case px-3 py-1 flex items-center rounded-lg shadow-sm"
        >
          <i class="mdi mdi-magnify mr-1 text-sm"></i>
          Apply
        </v-btn>
      </div>
    </div>
    <v-dialog v-model="showDeleteConfirm" max-width="400">
    <v-card class="border-b-4 border-darkred">
    <v-card-title class="text-lg font-bold">Confirm Delete</v-card-title>
    <v-card-text>
      Are you sure you want to delete all logs? This action cannot be undone.
    </v-card-text>
    <v-card-actions class="justify-end gap-2">
      <v-btn text @click="showDeleteConfirm = false">Cancel</v-btn>
      <v-btn color="darkred" @click="deleteAllLogs">Delete</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

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
const old_key = ref(null)
const old_val = ref(null)
const new_key = ref(null)
const new_val = ref(null)
const action_title = ref([]);
const showDeleteConfirm = ref(false);

const emit = defineEmits(["applyFilter", "deleteAll"])

const deleteAllLogs = () => {
  emit("deleteAll")
  showDeleteConfirm.value = false
}


const valueFields = [
  { label: "Username", value: "username" },
  { label: "Password", value: "password" },
  { label: "First Name", value: "first_name" },
  { label: "Last Name", value: "last_name" },
  { label: "Phone Number", value: "phone" },
  { label: "Email", value: "email" },
  { label: "Address", value: "address" },
  { label: "Active Status", value: "is_active" },
  { label: "Role", value: "role" },
];


const props = defineProps({
  usersList: {
    type: Array,
    default: () => [],
  },
});

const actionTypeMap = [
  { label: "Create User", value: "CREATE" },
  { label: "Update Profile", value: "UPDATE_PROFILE" },
  { label: "Delete User", value: "Delete user" },
  { label: "Delete All Logs", value: "DELETE_ALL_LOGS" },
  { label: "Delete Log", value: "Delete log" },
  { label: "Reset Locked Account", value: "Reset Locked Account" }
];


const confirmDeleteAllLogs = () => {
  showDeleteConfirm.value = true; 
};


const applyFilter = () => {
  const formatDate = (dateStr) => (dateStr ? new Date(dateStr).toISOString() : null);

  let stringifiedOldValues = null
  let stringifiedNewValues = null
    if (old_key.value && old_val.value) {
    stringifiedOldValues = JSON.stringify({
      [old_key.value]: old_key.value === 'is_active' 
        ? (old_val.value?.toString().trim() === 'true')
        : old_val.value
    })
  }
  if (new_key.value && new_val.value) {
    stringifiedNewValues = JSON.stringify({
      [new_key.value]: new_key.value === 'is_active' 
        ? (new_val.value?.toString().trim() === 'true')
        : new_val.value
    })
  }




emit("applyFilter", {
    username: username.value.length ? [...username.value] : null,
    start_time: formatDate(start_time.value),
    end_time: formatDate(end_time.value),
    old_values: stringifiedOldValues,
    new_values: stringifiedNewValues,
    action_title: action_title.value.length ? [...action_title.value] : null,
    search: searchQuery.value && searchQuery.value.trim() !== '' ? searchQuery.value : null,
    sortOrder: sortOrder.value === 'asc' ? 'action_time' : '-action_time'

});

};

const resetFilters = () => {
  username.value = [];
  start_time.value = null;
  end_time.value = null;
  old_key.value = null;
  old_val.value = null;
  new_key.value = null;
  new_val.value = null;
  searchQuery.value = null;
  action_title.value = [];

  emit("applyFilter", {
    username: null,
    start_time: null,
    end_time: null,
    old_values: null,
    new_values: null,
    action_title: null,
    search: null,
  });
};
const sortOrder = ref("desc")


</script>
