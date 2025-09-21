<script setup>
import TableLogs from '@/components/activity/TableLogs.vue'

const props = defineProps({
  filteredTimeline: { type: Array, required: true },
  page: { type: Number, required: true },
  limit: { type: Number, required: true }
})

const emit = defineEmits(['prevPage', 'nextPage', 'updateSort'])

</script>

<template>
  <div>
    <div class="table-wrapper flex flex-col h-[500px] w-full overflow-y-auto">
        <TableLogs :logs="filteredTimeline" @updateSort="$emit('updateSort', $event)" />
      </div>

    <div
      class="flex justify-center gap-2 p-2 sticky bottom-0 z-10 border-t-[1.5px] border-maincolor bg-white"
    >
      <v-btn
        @click="$emit('prevPage')"
        size="small"
        :disabled="page === 1"
        class="bg-lightblue text-maincolor hover:bg-maincolor hover:text-white text-xs normal-case px-4 py-2 flex items-center rounded-sm shadow-sm"
      >
        <i class="mdi mdi-chevron-left mr-1 text-sm"></i>
        Previous
      </v-btn>
      <v-btn
        @click="$emit('nextPage')"
        size="small"
        :disabled="filteredTimeline.length < limit"
        class="bg-lightblue text-maincolor hover:bg-maincolor hover:text-white text-xs normal-case px-4 py-2 flex items-center rounded-sm shadow-sm"
      >
        Next
        <i class="mdi mdi-chevron-right ml-1 text-sm"></i>
      </v-btn>
    </div>

  </div>
</template>
