<script>
import Timeline from '@/components/activity/Timeline.vue'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed } from 'vue'



const GET_TIMELINE = gql`
            query{
            allLogs{
                id
                actionType
                user{
                username
                }
                actionTime
                description
                
                
            }
            allAuthLogs{
                id
                actionType
                user{
                username
                }
                actionTime
                description
                
            }
            }
            `
    
export default {
  components: { Timeline },
  setup() {
    const { result, loading, error } = useQuery(GET_TIMELINE)
    const timelineItems = computed(() => {
      if (!result.value) return []
      return [
        ...(result.value.allLogs || []),
        ...(result.value.allAuthLogs || []),
      ]
    })

    return {
      timelineItems,
      loading,
      error,
    }
  },
}
</script>

<template>
  <div v-if="loading">در حال بارگذاری...</div>
  <div v-else-if="error">خطا: {{ error.message }}</div>
  <table v-else class="timeline-table">
    <tbody>
      <Timeline
        v-for="item in timelineItems"
        :key="item.id"
        :date="item.actionTime"
        :description="item.description"
        :user="item.user"
        :action="item.actionType"
      >
        {{ item.content }}
      </Timeline>
    </tbody>
  </table>
</template>


<style></style>

