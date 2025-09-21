<template>
    <div>
        <UsersFilter  :users="Users" @applyFilter="handleFilter"  />
        <div v-if="loading">Loading...</div>
        <div v-else-if="error"></div>
        <div v-else>
        <div class="flex flex-col h-[530px]">
          
        <v-table class="mt-4 mr-5 border border-gray-200 shadow w-full">
        <thead>
          <tr>
              <th class="text-left !bg-lightblue">User Name
                <button class="text-maincolor" @click="toggleSortOrder">
                  {{ sortOrder === 'asc' ? '↑' : '↓' }}
                </button>
              </th>
              <th class="text-left !bg-lightblue">First Name</th>
              <th class="text-left !bg-lightblue">Last Name</th>
              <th class="text-left !bg-lightblue">Email</th>
              <th class="text-left !bg-lightblue">Status</th>
              <th class="text-left !bg-lightblue">View</th>
              <th class="text-left !bg-lightblue">Actions</th>
              

            </tr>
        </thead>
        <tbody>
        <tr v-for="item in Users" :key="item.id" :class="{'font-bold': item.username === currentUsername }" >

            <td>
              <span v-if="item.role?.toLowerCase() === 'admin'" title="Admin" class="inline-block ml-2 text-maincolor">
                <UserCog class="w-4 h-4" /> 
              </span>
              <span v-else title="User" class="inline-block ml-2 text-darkbrown">
                <UserIcon class="w-4 h-4" />
              </span>
              {{ item.username }}
            </td>

            <td>{{ item.firstName }}</td>
            <td>{{ item.lastName }}</td>
            <td>{{ item.email }}</td>
            <td>
              <v-chip
                :color="item.isActive ? 'bg-lightgreen text-darkgreen' : 'bg-lightred text-darkred'"
                text-color="white"
              >
                {{ item.isActive ? 'Active' : 'Inactive' }}
              </v-chip>
                <v-chip
                  v-if="item.isLocked"
                  color="bg-lightgray text-darkbrown"
                  text-color="white"
                  class="ml-1"
                >
                  Locked
                </v-chip>
            </td>

            <td>
              <v-tooltip location="top">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon
                    variant="text"
                    @click="goToUser(item.username)"
                  >
                    <Eye class="w-5 h-5 stroke-[1.7] text-maincolor" />
                  </v-btn>
                </template>
                view user
              </v-tooltip>
            </td>

          <td>
            <v-tooltip location="top">
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon
                  variant="text"
                  @click="goToEditUser(item)"
                  :disabled="item.role?.toLowerCase() === 'admin' && item.username !== currentUsername"
                  :class="{'opacity-50 cursor-not-allowed': item.role?.toLowerCase() === 'admin' && item.username !== currentUsername}"
                >
                  <EditIcon class="w-5 h-5 stroke-[1.7] text-grayfont" />
                </v-btn>
              </template>
              Edit user
            </v-tooltip>

            <v-tooltip location="top">
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon
                  variant="text"
                  @click="() => { selectedUser = item; acceptDelete = true }"
                  :disabled="item.role?.toLowerCase() === 'admin' && item.username !== currentUsername"
                  :class="{'opacity-50 cursor-not-allowed': item.role?.toLowerCase() === 'admin' && item.username !== currentUsername}"
                >
                  <DeleteIcon class="w-5 h-5 stroke-[1.7] text-darkred" />
                </v-btn>
              </template>
              Delete user
            </v-tooltip>

            <v-tooltip v-if="item.isLocked" location="top">
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon
                  variant="text"
                  @click="resetLock(item.id)"
                  :disabled="item.role?.toLowerCase() === 'admin' && item.username !== currentUsername"
                >
                  <LockKeyholeOpen class="w-5 h-5 stroke-[1.7] text-grayfont" />
                </v-btn>

              </template>
              Unlock user
            </v-tooltip>
          </td>

          </tr>
        </tbody>
      </v-table>
      </div>
    <v-dialog v-model="acceptDelete" max-width="400">
      <v-card class="border-b-4 border-darkred">
        <v-card-title class="text-lg font-bold">Confirm Delete</v-card-title>
        <v-card-text v-if="selectedUser">
          Are you sure you want to delete <b>{{ selectedUser.username }}</b>?
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text @click="acceptDelete = false">Cancel</v-btn>
          <v-btn color="darkred" text @click="handleDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
      <div class="flex justify-center gap-2 p-2 sticky bottom-0 z-10 border-t-[1.5px] border-maincolor bg-white">
        <v-btn
          @click="prevPage"
          :disabled="page === 1"
          size="small"
          class="bg-lightblue text-maincolor hover:bg-maincolor hover:text-white text-xs normal-case px-4 py-2 flex items-center rounded-sm shadow-sm"
        >
          <i class="mdi mdi-chevron-left mr-1 text-sm"></i>
          Previous
        </v-btn>
        <v-btn
          @click="nextPage"
          :disabled="Users.length < tableLimit"
          size="small"
          class="bg-lightblue text-maincolor hover:bg-maincolor hover:text-white text-xs normal-case px-4 py-2 flex items-center rounded-sm shadow-sm"
        >
          Next
          <i class="mdi mdi-chevron-right ml-1 text-sm"></i>
        </v-btn>
      </div>
          </div>

    </div>
  
</template>
<script setup>
import { useQuery , useMutation } from '@vue/apollo-composable'
import { computed ,ref , onMounted, onBeforeUnmount ,onDeactivated } from 'vue'
import gql from 'graphql-tag' 
import { Eye, DeleteIcon ,EditIcon ,UserCog, UserIcon ,LockKeyholeOpen} from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import UsersFilter from '../filter/UsersFilter.vue'
import { useUserStore } from '@/stores/user'
import { useAlertStore } from '@/stores/alert'
const isAdminDisabled = computed(() =>
  props.role?.toLowerCase() === 'admin' && props.username !== currentUsername
)
const alertStore = useAlertStore()
const sortOrder = ref('desc')

const userStore = useUserStore()
const currentUsername = computed(() => userStore.username)


const router = useRouter()
const page = ref(1)
const tableLimit = ref(8)

const selectedUser = ref(null)
const acceptDelete = ref(false)
const emit = defineEmits(['edit', 'delete'])

 

const filters = ref({
  is_active: null,
  login_num: null,
  start_date: null,
  end_date: null,
  search: null,
})

const GET_ALLUSERS = gql`
        query GetAllUsers($search: String, $page: Int, $limit: Int, $loginNum: Int , $isActive: Boolean , $startDate: DateTime, $endDate: DateTime , $orderBy: String){
        allUsers(search:$search , page: $page, limit: $limit, loginNum: $loginNum ,isActive: $isActive , startDate: $startDate, endDate: $endDate ,orderBy:$orderBy ){
            username
            firstName
            lastName
            role
            email
            isActive
            id
            isLocked
            failedLoginAttempts
        }
        }`

const DELETE_USER = gql`
  mutation DeleteUser($id: ID!) {
    deleteUser(id: $id) {
      ok
    }
  }
`
const RESET_LOCK = gql`
  mutation ResetLock($userId: ID!) {
    resetLock(userId: $userId) {
      success
      message
    }
  }
`

const { mutate: resetLockMutation } = useMutation(RESET_LOCK)

const { mutate: deleteUserMutation } = useMutation(DELETE_USER)

onBeforeUnmount(() => {
  document.querySelectorAll('.v-overlay-container, .v-tooltip').forEach(el => el.remove())

})
onDeactivated(() => {
  document.querySelectorAll('.v-overlay-container, .v-tooltip').forEach(el => el.remove())
})        

const variables = computed( () =>({
  page : page.value,
  limit : tableLimit.value,
  loginNum : filters.value.login_num,
  isActive : filters.value.is_active,
  startDate: filters.value.start_date,
  endDate: filters.value.end_date,
  search: filters.value.search,
  orderBy: sortOrder.value === 'asc' ? 'created_at' : '-created_at'

})
)
const {result, loading, error , refetch} = useQuery(GET_ALLUSERS , variables)

const deleteUser = async (id) => {
  try {
    const { data } = await deleteUserMutation({ id })
    if (data.deleteUser.ok) {
      refetch(variables.value)
      alertStore.show('User deleted successfully!', 'success')
    } else {
      alertStore.show('Failed to delete user.', 'error')
    }
  } catch (err) {
    alertStore.show(`Delete error: ${err.message}`, 'error')
  }
}

const handleDelete = async () => {
  if (!selectedUser.value) return
  const id = selectedUser.value.id
  acceptDelete.value = false
  selectedUser.value = null
  await deleteUser(id)
  emit('delete', id)
}
const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  page.value = 1
  refetch(variables.value)  
}

const Users = computed(() => result.value?.allUsers || [])


const resetLock = async (id) => {
  try {
    const { data } = await resetLockMutation({ userId: id })
    if (data.resetLock.success) {
      console.log("User unlocked:", id)
      refetch(variables.value)
    } else {
      console.error("Reset lock failed:", data.resetLock.message)
    }
  } catch (err) {
    console.error("Reset lock error:", err.message)
  }
}


const handleFilter =(newfilters) =>{
  filters.value = newfilters
  page.value = 1
  refetch(variables.value)
}

const prevPage = () => {
  if (page.value > 1) {
    page.value -= 1
    refetch(variables.value)
  }
}

const nextPage = () => {
  page.value += 1
  refetch(variables.value)
}


 const goToUser = (username) => {
  router.push(`/userpanel/${username}`)
}

const goToEditUser = (user) => {
  router.push({ 
    name: 'userpanel',
    params: { username: user.username }, 
    query: { id: user.id, edit: true } 
  })
}



</script>
