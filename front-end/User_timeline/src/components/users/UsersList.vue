<template>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error.message }}</div>
    <div v-else>
      <v-table class="mt-8 mr-5">
    <thead>
      <tr>
          <th class="text-left !bg-lightblue">User Name</th>
          <th class="text-left !bg-lightblue">First Name</th>
          <th class="text-left !bg-lightblue">Last Name</th>
          <th class="text-left !bg-lightblue">Email</th>
          <th class="text-left !bg-lightblue">Status</th>
          <th class="text-left !bg-lightblue">View</th>
          <th class="text-left !bg-lightblue">Actions</th>

        </tr>
    </thead>
    <tbody>
      <tr
        v-for="item in Users"
        :key="item.username"
      >
        <td>
          <span v-if="item.role.toLowerCase() === 'admin'" title="Admin" class="inline-block ml-2 text-maincolor">
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

        </td>

        <td>
            <v-btn
              icon
              variant="text"
              @click="goToUser(item.username)"
            >
                  <v-tooltip
                    activator="parent"
                    location="top"
                  >view user</v-tooltip>
              <Eye class="w-5 h-5 stroke-[1.7] text-maincolor" />
            </v-btn>
          </td>

          <td>
            <v-btn icon variant="text" @click="goToEditUser(item.username)">
              <EditIcon class="w-5 h-5 stroke-[1.7] text-grayfont" />
            </v-btn>
            <v-btn icon variant="text" @click="deleteUser(item.username)">
              <DeleteIcon class="w-5 h-5 stroke-[1.7] text-grayfont" />
            </v-btn>
          </td>
      </tr>
    </tbody>
  </v-table>
    </div>

</template>
<script setup>
import { useQuery } from '@vue/apollo-composable'
import { computed } from 'vue'
import gql from 'graphql-tag' 
import { Eye, DeleteIcon ,EditIcon ,UserCog, UserIcon } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()


const GET_ALLUSERS = gql`
        query{
        allUsers{
            username
            firstName
            lastName
            role
            email
            isActive
        }
        }`

const {result, loading, error} = useQuery(GET_ALLUSERS)

const Users = computed(() =>{
    return result.value?.allUsers || {};}
)
 
 const goToUser = (username) => {
  router.push(`/userpanel/${username}`)
}

const goToEditUser = (username) => {
  router.push({ 
    name: 'userpanel',      
    params: { username },      
    query: { edit: true }       
  })
}
</script>
