<script setup>
import TimelineComponent from '@/components/activity/TimelineComponent.vue'
import TableLogsComponent from './TableLogsComponent.vue'
import AllLogsFilter from '../filter/AllLogsFilter.vue'
import ManagementLogsFilter from '../filter/ManagementLogsFilter.vue'
import AuthLogsFilter from '../filter/AuthLogsFilter.vue'
import { useQuery, useMutation } from '@vue/apollo-composable'

import gql from 'graphql-tag'
import { computed, defineProps, ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { formatDistanceToNow, parseISO, format } from 'date-fns'
import { DoorClosed, DoorOpen, UserPlus, Trash2, PencilLine, HelpCircle, LockKeyholeOpen, LockKeyhole, TriangleAlert,ListX } from 'lucide-vue-next'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()


const props = defineProps({
  username: { type: String, default: null },
  onlyAuth: { type: Boolean, default: false },
  onlyManagement: { type: Boolean, default: false },
  isTableView: { type: Boolean, default: false }
})


const filters = ref({
  start_time: null,
  end_time: null,
  action_title: null,
  old_values: null,
  new_values: null,
  username: null,
  category: null,
  search: null,
  sortOrder: null,
})


const timelineLogs = ref([])
const timelinePage = ref(1)
const timelineLimit = ref(8)
const timelineIsLastPage = ref(false)
const scrollContainer = ref(null)
const timelineScrollLoading = ref(false)


const tableLogs = ref([])
const tablePage = ref(1)
const tableLimit = ref(11)
const tableIsLastPage = ref(false)


const GET_ALL_LOGS = gql`
query GetCombinedLogs($search:String , $page: Int, $limit: Int, $username: [String] , $startTime: DateTime , $endTime: DateTime, $actionTitle: [String] , $oldValues: GenericScalar , $newValues: GenericScalar , $category : String ,$orderBy: String) {
  allLogsCombined(search: $search ,page: $page, limit: $limit, username: $username , startTime: $startTime , endTime: $endTime, actionTitle: $actionTitle , oldValues: $oldValues , newValues:$newValues , category: $category, orderBy:$orderBy) {
    logId
    actionType
    actionTime
    actionTitle
    description
    category
    isProtected
    user { id username firstName lastName email }
    actorUser { id username firstName lastName email }
    targetUser { id username firstName lastName email }
  }
}
`
const GET_AUTH_LOGS = gql`
query GetAuthLogs($search:String, $page: Int, $limit: Int, $username: [String] , $startTime: DateTime , $endTime: DateTime, $actionTitle: [String], $orderBy: String ) {
  authLogs(search: $search, page: $page, limit: $limit , username: $username , startTime: $startTime , endTime: $endTime, actionTitle: $actionTitle,orderBy:$orderBy) {
    id
    actionType
    actionTime
    actionTitle
    description
    user { id role username firstName lastName }
  }
}
`
const GET_MANAGEMENT_LOGS = gql`
query GetManagementLogs($search:String, $page: Int, $limit: Int, $username: [String] , $startTime: DateTime , $endTime: DateTime, $actionTitle: [String] , $oldValues: GenericScalar , $newValues: GenericScalar ,$orderBy: String) {
  logs(search: $search, page: $page, limit: $limit, username: $username , startTime: $startTime , endTime: $endTime, actionTitle: $actionTitle , oldValues: $oldValues , newValues:$newValues, orderBy:$orderBy ) {
    id
    actionType
    actionTime
    actionTitle
    description
    isProtected
    actorUser { id role username }
    targetUser { id role username }
  }
}
`
const GET_ALL_USERS = gql`
  query GetAllUsers($page: Int, $limit: Int, $orderBy: String) {
    allUsers(page: $page, limit: $limit, orderBy:$orderBy) {
      id
      username
      firstName
      lastName
    }
  }
`

const DELETE_ALL_LOGS = gql`
mutation {
  deleteAllLog {
    deleteAll
    message
  }
}

`

const DELETE_LOG = gql`
mutation DeleteLog($id: ID!) {
  deleteLog(id: $id) {
    ok
    message
  }
}
`

const { mutate: deleteLogMutation, loading: deleteLogLoading } = useMutation(DELETE_LOG)



const { result: usersResult } = useQuery(GET_ALL_USERS)
const usersList = computed(() => usersResult.value?.allUsers || [])


const currentQuery = computed(() =>
  props.onlyAuth ? GET_AUTH_LOGS : props.onlyManagement ? GET_MANAGEMENT_LOGS : GET_ALL_LOGS
)

const { mutate: deleteAllLogsMutation, loading: deleteLoading } = useMutation(DELETE_ALL_LOGS)

const timelineVariables = computed(() => {
  const vars = { page: timelinePage.value, limit: timelineLimit.value }
  applyFilter(vars)
  return vars
})

const tableVariables = computed(() => {
  const vars = { page: tablePage.value, limit: tableLimit.value }
  applyFilter(vars)
  return vars
})



function applyFilter(vars) {
  if (props.username && props.username.trim() && props.username !== "null" && props.username !== "undefined") vars.username = [props.username]
  if (filters.value.start_time) vars.startTime = filters.value.start_time
  if (filters.value.end_time) vars.endTime = filters.value.end_time
  if (filters.value.action_title?.length > 0) vars.actionTitle = [...filters.value.action_title]
  if (filters.value.old_values) vars.oldValues = filters.value.old_values
  if (filters.value.new_values) vars.newValues = filters.value.new_values
  if (filters.value.category) vars.category = filters.value.category
  if (filters.value.username) vars.username = Array.isArray(filters.value.username) ? filters.value.username.map(String) : [String(filters.value.username)]
  if (filters.value.search?.trim()) vars.search = filters.value.search
  if (filters.value.sortOrder) vars.orderBy = filters.value.sortOrder

}


const { result: timelineResult, loading: timelineLoading, refetch: refetchTimeline } = useQuery(currentQuery, timelineVariables)
const { result: tableResult, loading: tableLoading, refetch: refetchTable } = useQuery(currentQuery, tableVariables)

watch(timelineResult, (newVal) => {
  if (!newVal) return
  const data = props.onlyAuth ? newVal.authLogs || [] :
               props.onlyManagement ? newVal.logs || [] :
               newVal.allLogsCombined || []
  timelineLogs.value = timelinePage.value === 1 ? data : [...timelineLogs.value, ...data]
  if (data.length < timelineLimit.value) timelineIsLastPage.value = true
})

watch(tableResult, (newVal) => {
  if (!newVal) return
  const data = props.onlyAuth ? newVal.authLogs || [] :
               props.onlyManagement ? newVal.logs || [] :
               newVal.allLogsCombined || []
  tableLogs.value = data
  tableIsLastPage.value = data.length < tableLimit.value
})


function handleFilter(newFilters) {
  filters.value = { ...newFilters }
  timelinePage.value = 1
  tablePage.value = 1
  refetchTimeline()
  refetchTable()
}

async function handleDeleteAll() {
  try {
    const res = await deleteAllLogsMutation()
    const response = res?.data?.deleteAllLog

    if (response) {
      if (response.deleteAll) {
        alertStore.show(response.message || "All logs deleted successfully", "success")
      } else {
        alertStore.show(response.message || "No logs deleted (protected logs remain)", "warning")
      }
    } else {
      alertStore.show("Unexpected response from server", "error")
    }

    timelineLogs.value = []
    tableLogs.value = []
    timelinePage.value = 1
    tablePage.value = 1
    timelineIsLastPage.value = false
    tableIsLastPage.value = false

    refetchTimeline()
    refetchTable()
  } catch (err) {
    console.error("Delete logs error:", err)
    alertStore.show("Server error while deleting logs", "error")
  }
}

async function handleDeleteLog(logId) {
  try {
    console.log('Deleting log with ID:', logId); // <-- اینجا ID لاگ رو چاپ می‌کنیم
    
    const res = await deleteLogMutation({ id: logId });
    
    console.log('Server response:', res); // <-- پاسخ سرور رو چاپ می‌کنیم

    const response = res?.data?.deleteLog;

    if (response?.ok) {
      alertStore.show(response.message || "Log deleted successfully", "success");
      
      // Filter out the deleted log from the local arrays
      timelineLogs.value = timelineLogs.value.filter(log => log.logId !== logId);
      tableLogs.value = tableLogs.value.filter(log => log.logId !== logId);

      // Refetch
      refetchTimeline();
      refetchTable();
      
    } else {
      alertStore.show(response?.message || "Cannot delete log", "error");
    }
  } catch (err) {
    console.error('Delete log error:', err);
    alertStore.show("Server error while deleting log", "error");
  }
}


watch(() => props.username, () => handleFilter(filters.value))
watch(() => [props.onlyAuth, props.onlyManagement], () => handleFilter(filters.value))
watch(tableLimit, () => { if (props.isTableView) refetchTable() })


onMounted(() => { if (scrollContainer.value) scrollContainer.value.addEventListener('scroll', handleScroll) })
onBeforeUnmount(() => { if (scrollContainer.value) scrollContainer.value.removeEventListener('scroll', handleScroll) })

async function handleScroll(e) {
  const el = e.currentTarget
  if (!timelineScrollLoading.value && !timelineIsLastPage.value && el.scrollTop + el.clientHeight >= el.scrollHeight - 50) {
    timelinePage.value++
    timelineScrollLoading.value = true
    await refetchTimeline()
    timelineScrollLoading.value = false
  }
}



function prevTablePage() { if (tablePage.value > 1) { tablePage.value--; refetchTable() } }
function nextTablePage() { tablePage.value++; refetchTable() }



const getIconComponent = (actionType) => {
  const iconMap = { LOGIN: DoorOpen, LOGOUT: DoorClosed, CREATE: UserPlus, DELETE_USER: Trash2, DELETE_ALL_LOGS: Trash2, UPDATE_PROFILE: PencilLine, RESET_LOCK: LockKeyholeOpen, LOGIN_FAILED: TriangleAlert, LOCK_USER: LockKeyhole,
    DELETE_LOG: ListX
   }
  return iconMap[(actionType || '').toUpperCase()] || HelpCircle
}

const parseDescription = (desc) => { try { return JSON.parse(desc) || {} } catch { return {} } }
const changedate = (isostring) => isostring ? formatDistanceToNow(parseISO(isostring), { addSuffix: true }).replace(/^about /, '') : ''
const formatExact = (isostring) => isostring ? format(parseISO(isostring), 'HH:mm|dd MMM yyyy') : ''

const filteredTimeline = computed(() => timelineLogs.value.map(item => {
  const parsedDesc = parseDescription(item.description)
  const user = item.user || item.actorUser || {}     
  const targetUser = item.targetUser || parseDescription(item.description).user_snapshot || {}

  return {
    ...item,
    logId: item.logId || item.id,
    description: parsedDesc.message || item.description || '',
    fieldsChanged: parsedDesc.fields_changed || null,
    userProp: user,
    targetuserProp: targetUser,
    icon: getIconComponent(item.actionType),
    relativeDate: changedate(item.actionTime),
    exactDate: formatExact(item.actionTime),
    category: item.category || (props.onlyAuth ? 'Authentication' : props.onlyManagement ? 'Management' : null),
    isProtected: item.isProtected || false
  }
}))


const filteredTable = computed(() => tableLogs.value.map(item => {
  const parsedDesc = parseDescription(item.description)
  const user = item.user || item.actorUser || {}
  const targetUser = item.targetUser || parseDescription(item.description).user_snapshot || {}
  return {
    ...item,
    logId: item.logId || item.id,
    description: parsedDesc.message || item.description || '',
    fieldsChanged: parsedDesc.fields_changed || null,
    userProp: user,
    targetuserProp: targetUser,
    icon: getIconComponent(item.actionType),
    relativeDate: changedate(item.actionTime),
    exactDate: formatExact(item.actionTime),
    category: item.category || (props.onlyAuth ? 'Authentication' : props.onlyManagement ? 'Management' : null),
    isProtected: item.isProtected || false
  }
}))

</script>

<template>
  <div class="activitylog">
    <div v-if="usersList.length">
      <AllLogsFilter v-if="!props.onlyAuth && !props.onlyManagement" :usersList="usersList" @applyFilter="handleFilter" @deleteAll="handleDeleteAll"/>
      <AuthLogsFilter v-else-if="props.onlyAuth" :usersList="usersList" @applyFilter="handleFilter" />
      <ManagementLogsFilter v-else-if="props.onlyManagement" :usersList="usersList" @applyFilter="handleFilter" @deleteAll="handleDeleteAll" />
    </div>

    <div v-if="!props.isTableView" ref="scrollContainer" class="timeline-scroll-container" style="max-height: 600px; overflow-y: auto;">
      <TimelineComponent :filteredTimeline="filteredTimeline" :loading="timelineLoading" :isLastPage="timelineIsLastPage"
      @deleteLog="handleDeleteLog" @updateSort="handleUpdateTimelineSort" />
      <div v-if="timelineLoading" class="flex justify-center py-4 text-gray-500"><span class="animate-pulse">Loading more logs...</span></div>
      <div v-if="timelineIsLastPage && !timelineLoading" class="flex justify-center py-4 text-gray-500"><p>End of the list.</p></div>
    </div>

    <div v-else class="flex flex-col min-h-[calc(100vh-120px)] justify-between pb-20">
      <TableLogsComponent
        :filteredTimeline="filteredTable"
        :loading="tableLoading"
        :page="tablePage"
        :limit="tableLimit"
        @prevPage="prevTablePage"
        @nextPage="nextTablePage"
        @updateSort="handleUpdateSort"
      />

    </div>
  </div>
</template>
