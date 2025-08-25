<script setup>
import Timeline from '@/components/activity/TimeLine.vue'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed, defineProps, ref, watch } from 'vue'
import { formatDistanceToNow, parseISO, format } from 'date-fns'
import { LogIn, LogOut, UserPlus, Trash2, PencilLine, HelpCircle } from 'lucide-vue-next'

const page = ref(1)
const limit = ref(10)
const isLastPage = ref(false)

const props = defineProps({
  username: { type: String, default: null },
  onlyAuth: { type: Boolean, default: false },
  onlyManagement: { type: Boolean, default: false }
})

const GET_TIMELINE = gql`
query GetCombinedLogs($page: Int, $limit: Int) {
  allLogsCombined(page: $page, limit: $limit) {
    logId
    actionType
    actionTime
    actionTitle
    description
    category
    user { id username firstName lastName email }
    actorUser { id username firstName lastName email }
    targetUser { id username firstName lastName email }
  }
}
`
const GET_AUTH_LOGS = gql`
query GetAuthLogs($page: Int, $limit: Int) {
  authLogs(page: $page, limit: $limit) {
    id
    actionType
    actionTime
    actionTitle
    description
    user { id username firstName lastName }
  }
}
`;

const GET_MANAGEMENT_LOGS = gql`
query GetManagementLogs($page: Int, $limit: Int) {
  logs(page: $page, limit: $limit) {
    id
    actionType
    actionTime
    actionTitle
    description
    actorUser { id username }
    targetUser { id username }
  }
}
`;

const currentQuery = computed(() => {
  if (props.onlyAuth) return GET_AUTH_LOGS;
  if (props.onlyManagement) return GET_MANAGEMENT_LOGS;
  return GET_TIMELINE;
});

const { result, loading, error, fetchMore, refetch } = useQuery(currentQuery, {
  page: page.value,
  limit: limit.value
});

watch(() => [props.onlyAuth, props.onlyManagement], () => {
  page.value = 1;
  isLastPage.value = false;
  refetch();
});

const handleScroll = async (e) => {
  const el = e.currentTarget;

  if (!loading.value && !isLastPage.value && (el.scrollTop + el.clientHeight >= el.scrollHeight - 10)) {
    page.value += 1;
     
    try {
      await fetchMore({
        variables: {
          page: page.value,
          limit: limit.value
        },
        updateQuery: (previousResult, { fetchMoreResult }) => {
          if (!fetchMoreResult) {
            isLastPage.value = true;
            return previousResult;
          }

          let updatedResult;
          if (props.onlyAuth) {
            const newData = fetchMoreResult?.authLogs || [];
            if (newData.length < limit.value) isLastPage.value = true;
            updatedResult = {
              ...previousResult,
              authLogs: [
                ...(previousResult?.authLogs || []),
                ...newData
              ]
            };
          } else if (props.onlyManagement) {
            const newData = fetchMoreResult?.logs || [];
            if (newData.length < limit.value) isLastPage.value = true;
            updatedResult = {
              ...previousResult,
              logs: [
                ...(previousResult?.logs || []),
                ...newData
              ]
            };
          } else {
            const newData = fetchMoreResult?.allLogsCombined || [];
            if (newData.length < limit.value) isLastPage.value = true;
            updatedResult = {
              ...previousResult,
              allLogsCombined: [
                ...(previousResult?.allLogsCombined || []),
                ...newData
              ]
            };
          }
          return updatedResult;
        }
      });
    } catch (err) {
      console.error("Error fetching more data:", err);
    }
  }
}

const getIconComponent = (actiontype) => {
  const iconMap = {
    LOGIN: LogIn,
    LOGOUT: LogOut,
    CREATE: UserPlus,
    DELETE: Trash2,
    DELETE_ALL_LOGS: Trash2,
    UPDATE_PROFILE: PencilLine,
  };
  return iconMap[(actiontype || '').toUpperCase()] || HelpCircle;
}

const parseDescription = (desc) => {
  try { return JSON.parse(desc) } catch { return null }
}

const changedate = (isostring) => {
  if (!isostring) return ''
  return formatDistanceToNow(parseISO(isostring), { addSuffix: true }).replace(/^about /, '')
}

const formatExact = (isostring) => {
  if (!isostring) return ''
  return format(parseISO(isostring), 'HH:mm|dd MMM yyyy')
}

const filteredTimeline = computed(() => {
  let data = [];
  let categoryOverride = null;

  if (props.onlyAuth) {
    data = result.value?.authLogs ?? [];
    categoryOverride = "Authentication";
  } else if (props.onlyManagement) {
    data = result.value?.logs ?? [];
    categoryOverride = "Management";
  } else {
    data = result.value?.allLogsCombined ?? [];
  }

  return data
    .filter(item => {
      if (props.username) {
        if (props.onlyAuth) return item.user?.username === props.username;
        if (props.onlyManagement) return item.actorUser?.username === props.username || item.targetUser?.username === props.username;
        if (item.category === "Authentication") return item.user?.username === props.username;
        if (item.category === "Management") return item.actorUser?.username === props.username || item.targetUser?.username === props.username;
      }
      return true;
    })
    .map(item => {
      const parsedDesc = parseDescription(item.description) || {}
      return {
        ...item,
        logId: item.logId || item.id,
        description: parsedDesc.message || item.description || '',
        fieldsChanged: parsedDesc.fields_changed || null,
        userProp: item.user || item.actorUser,
        targetuserProp: item.targetUser || null,
        icon: getIconComponent(item.actionType),
        relativeDate: changedate(item.actionTime),
        exactDate: formatExact(item.actionTime),
        category: item.category || categoryOverride
      }
    })
})
</script>

<template>
  <div class="activitylog">
    <div v-if="loading && filteredTimeline.length === 0" class="text-center text-grayfont py-4"> Loading ...</div>
    <div v-else-if="error" class="text-center text-darkred py-4">Error: {{ error.message }}</div>
    <div v-else class="timeline-table overflow-y-auto max-h-[600px]" @scroll="handleScroll">
      <Timeline 
        v-for="item in filteredTimeline" 
        :key="item.logId" 
        :date="changedate(item.actionTime)" 
        :description="item.description" 
        :action="item.actionTitle" 
        :fields-changed="item.fieldsChanged" 
        :category="item.category" 
        :relative-date="item.relativeDate" 
        :user="item.userProp" 
        :targetUser="item.targetuserProp" 
        :icon="item.icon" 
      />
      <div v-if="filteredTimeline.length > 0 && isLastPage" class="text-center text-grayfont py-4">
        End of list
      </div>
      <div v-if="loading && filteredTimeline.length > 0" class="text-center text-grayfont py-4"> 
        Loading more ... 
      </div>
    </div>
  </div>
</template>