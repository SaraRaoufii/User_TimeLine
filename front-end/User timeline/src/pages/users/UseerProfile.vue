<script>
import Timeline from '@/components/activity/Timeline.vue'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed } from 'vue'
import { h } from 'vue'
import { formatDistanceToNow, parseISO } from 'date-fns'
import { LogIn, LogOut, UserPlus, Trash2, PencilLine, HelpCircle } from 'lucide-vue-next'
import { format } from 'date-fns'



const GET_TIMELINE = gql`
            query{
            allLogs{
                id
                actionType
                actionTitle
                actorUser{
                  id
                  username
                  firstName
                  lastName
                  email
                  role
                }
                targetUser{
                  id
                  username
                  firstName
                  lastName
                  email
                  role
                }
                actionTime
                description
                
                
            }
            allAuthLogs{
                id
                actionType
                actionTitle
                user{
                  id
                  username
                  firstName
                  lastName
                  email
                  role
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

    const getIconComponent = (actiontype) =>{
      const iconMap = {
        LOGIN: LogIn,
        LOGOUT: LogOut,
        CREATE: UserPlus,
        DELETE: Trash2,
        DELETE_ALL_LOGS: Trash2,
        UPDATE_PROFILE: PencilLine,
      }
      const IconComponent = iconMap[actiontype] || HelpCircle

      return h(IconComponent, {
        class: 'icon-only',  
        strokeWidth: 1.5   
      })
    }
    
    const timelineItems = computed(() => {
      if (!result.value) return []
      return [
        ...(result.value.allLogs || []),
        ...(result.value.allAuthLogs || []),
      ]
    })

    const filtertimeline = computed( () => {
        const parseDescription = (desc) => {
          try {
            return JSON.parse(desc)
          } catch {
            return null
          }
        }
      return timelineItems.value.map(item =>{
         const parsedDesc = parseDescription(item.description) || {}
        return{
          ...item,

          description: parsedDesc.message || item.description || '',

          fieldsChanged: parsedDesc.fields_changed || null,

          userProp:(item.actionType =="LOGIN" || item.actionType =="LOGOUT")
          ?item.user
          :item.actorUser,

          category: item.category || (item.actionType === "LOGIN" || item.actionType === "LOGOUT" ? 'Authentication' : 'Management'),

          targetuserProp: (item.actionType =="LOGIN" || item.actionType =="LOGOUT")
          ? null
          :item.targetUser,

          icon: getIconComponent(item.actionType),

          relativeDate: changedate(item.actionTime),

          exactDate: formatExact(item.actionTime),   
          

     
        }
      })
    })

    const changedate = (isostring) =>{
      if (!isostring) return ''

      const date= parseISO(isostring)
      const result= formatDistanceToNow(date ,{addSuffix:true})
      return result.replace(/^about /, '')
    }

    const formatExact = (isostring) => {
      if (!isostring) return ''
      const date = parseISO(isostring)
      return format(date, 'HH:mm|dd MMM yyyy')
    }



    return {
      timelineItems:filtertimeline,
      loading,
      error,
      changedate,
      formatExact,
    }
  },


}
</script>

<template>
  <div v-if="loading">در حال بارگذاری...</div>
  <div v-else-if="error">خطا: {{ error.message }}</div>
  <div v-else class="timeline-table">
      <Timeline
        v-for="item in timelineItems"
        :key="item.id"
        :date="changedate(item.actionTime)"
        :description="item.description"
        :action="item.actionTitle"
        :fields-changed="item.fieldsChanged"
        :category="item.category"
        :relative-date="item.relativeDate"
        :user="item.userProp"
        :targetUser="item.targetuserProp"
        :icon="item.icon"
      >
      </Timeline>
            <!-- <Timeline
        v-for="item in timelineItems"
        :key="item.id"
        :date="changedate(item.actionTime)"
        :description="item.description"
        :action="item.actionTitle"
        :fields-changed="item.fieldsChanged"
        :category="item.category"
        :relative-date="item.relativeDate"
        :exact-date="item.exactDate"
        :user="item.userProp"
        :targetUser="item.targetuserProp"
        :icon="item.icon"
        :is-auth-log="item.isAuthLog"
      >
      </Timeline> -->
    </div>
</template>


<style></style>

