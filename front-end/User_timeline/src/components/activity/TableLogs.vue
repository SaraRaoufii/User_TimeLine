<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <div v-else class="h-full">

    <table
      v-if="logs.length && logs[0].category === 'Authentication'"
      class="min-w-full divide-y divide-gray-200"
    >
      <thead class="bg-lightblue sticky top-0 z-10">
        <tr>
          <th class="px-4 py-2 text-left font-semibold">Actor</th>
          <th class="px-4 py-2 text-left font-semibold">Action</th>
          <th class="px-4 py-2 text-left font-semibold">Time</th>

          <th class="px-4 py-2 text-left font-semibold">Description</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200 text-sm">
        <tr
          v-for="log in logs"
          :key="log.logId"
          class="hover:bg-gray-50"
        >
          <td class="px-4 py-2">
            <div class="flex items-center gap-2">
              <UserCog
                v-if="log.userProp?.role?.toLowerCase() === 'admin'"
                class="w-4 h-4 text-maincolor"
              />
              <UserIcon v-else class="w-4 h-4 text-darkbrown" />
              <span>{{ log.userProp?.username || 'N/A' }}</span>
            </div>
          </td>
          <td class="px-4 py-2">{{ log.actionTitle }}</td>
          <td class="px-4 py-2">{{ log.exactDate || log.relativeDate }}</td>
          <td class="px-4 py-2">{{ log.description }}</td>
        </tr>
      </tbody>
    </table>

    <table
      v-else-if="logs.length && logs[0].category === 'Management'"
      class="min-w-full divide-y divide-gray-200"
    >
      <thead class="bg-lightblue sticky top-0 z-10">
        <tr>
          <th class="px-4 py-2 text-left font-semibold">Actor</th>
          <th class="px-4 py-2 text-left font-semibold">Target</th>
          <th class="px-4 py-2 text-left font-semibold">Action</th>
          <th class="px-4 py-2 text-left font-semibold">Time</th>
          <th class="px-4 py-2 text-left font-semibold">Description</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200 text-sm">
        <tr
          v-for="log in logs"
          :key="log.logId"
          class="hover:bg-gray-50"
        >
          <td class="px-4 py-2">
            <div class="flex items-center gap-2">
              <UserCog
                v-if="log.userProp?.role?.toLowerCase() === 'admin'"
                class="w-4 h-4 text-maincolor"
              />
              <UserIcon v-else class="w-4 h-4 text-darkbrown" />
              {{ log.userProp?.username || 'N/A' }}
            </div>
          </td>
          <td class="px-4 py-2">
            <div class="flex items-center gap-2">
              <UserCog
                v-if="log.targetuserProp?.role?.toLowerCase() === 'admin'"
                class="w-4 h-4 text-maincolor"
              />
              <UserIcon v-else class="w-4 h-4 text-darkbrown" />
              {{ log.targetuserProp?.username || 'N/A' }}
            </div>
          </td>
          <td class="px-4 py-2">{{ log.actionTitle }}</td>
          <td class="px-4 py-2">{{ log.exactDate || log.relativeDate }}</td>
          <td class="px-4 py-2">
            <div class="flex flex-col">
              <div class="flex items-center">
                <span class="ml-2">{{ log.description }}</span>
              </div>
              <div
                v-for="(change, field) in log.fieldsChanged"
                :key="field"
                class="inline-flex flex-wrap items-center m-1 mt-1"
              >
                <strong class="text-maincolor mr-1">{{ field }}:</strong>
                <span class="bg-lightred line-through px-1 rounded">{{ change.old_val }}</span>
                <MoveRight class="w-4 h-4 text-maincolor mx-1" />
                <span class="bg-lightgreen px-1 rounded">{{ change.new_val }}</span>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { UserCog, UserIcon, MoveRight } from 'lucide-vue-next'
import { ref } from 'vue'

const props = defineProps({
  loading: { type: Boolean, default: false },
  error: { type: Object, default: null },
  logs: { type: Array, default: () => [] },
})

const emit = defineEmits(['updateSort'])

const localSort = ref('desc')

function toggleSortOrder() {
  localSort.value = localSort.value === 'asc' ? 'desc' : 'asc'
  emit('updateSort', localSort.value)
}

</script>
