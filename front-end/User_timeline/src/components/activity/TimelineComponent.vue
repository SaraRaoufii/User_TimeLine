<script setup>
import Timeline from '@/components/activity/TimeLine.vue'
import { computed } from 'vue'

const props = defineProps({
  filteredTimeline: { type: Array, required: true },
})
</script>

<template>
  <div class="timeline-inner flex flex-col gap-2.5 mb-8 ">
    <Timeline 
      v-for="item in filteredTimeline" 
      :key="item.logId"
      :date="item.date" 
      :description="item.description" 
      :action="item.actionTitle" 
      :fields-changed="item.fieldsChanged" 
      :category="item.category" 
      :relative-date="item.relativeDate" 
      :user="item.userProp || {}" 
      :targetUser="item.targetuserProp || {}" 
      :icon="item.icon" 
      :isProtected="item.isProtected"
      :log-id="item.logId"            
      @deleteLog="$emit('deleteLog', $event)" 
    />
  </div>
</template>
