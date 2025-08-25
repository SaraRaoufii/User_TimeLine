<template>
  <div class="userinfo p-6  w-full max-w-none">
    <div class="first_row flex items-center gap-4 mb-6">

      <div :class="[
          'role flex justify-center items-center rounded-full w-[70px] h-[32px] px-3 font-semibold',
          role.toLowerCase() === 'admin' ? 'text-maincolor bg-lightblue' : 'text-darkbrown bg-lightbrown'
        ]">
        {{ role }}
      </div>

      <div :class="[
          'active flex justify-center items-center rounded-full w-[70px] h-[32px] px-3 font-semibold',
          isActive ? 'bg-lightgreen text-darkgreen' : 'bg-lightred text-darkred'
        ]">
        {{ isActive ? 'Active' : 'Inactive' }}
      </div>
    </div>

    <div class="info_items ml-6 grid grid-cols-1 sm:grid-cols-2 gap-x-10 gap-y-4">
      <div class="username">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Username:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4">{{ username }}</p>
      </div>

      <div class="first_name">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">First Name:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4">{{ firstName }}</p>
      </div>

      <div class="last_name">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Last Name:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4">{{ lastName }}</p>
      </div>

      <div class="password">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Password:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4">{{ password }}</p>
      </div>

      <div class="email">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Email:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4">{{ email }}</p>
      </div>

      <div class="phonenumber">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Phone Number:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4">{{ phone }}</p>
      </div>

      <div class="adress">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Address:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4">{{ address }}</p>
      </div>
    </div>
    <div class="btn flex flex-row gap-3 ml-2">
    <v-btn size="small" class="button bg-maincolor text-[#FEFCF4]" @click="$emit('edit')">
      <UserRoundPen class="stroke-[1.5] w-[18px] h-[18px] mr-1"/>
      Edit User
    </v-btn>

    <v-btn size="small" class="button border-maincolor text-maincolor ">
        <UserRoundMinus class="stroke-[1.5] w-[18px] h-[18px] mr-1"/>
    Delet User
    </v-btn>
    </div>

  </div>
</template>

<script setup>
import { UserRoundPen, UserRoundMinus } from 'lucide-vue-next';
defineProps({
    username: {
        type: String,
        required: true,
    },

    firstName: {
        type: String,
    },
    
    lastName: {
        type: String,
    },

    password: {
        type: String,
    }, 

    phone: { 
        type: String,
    }, 

    email: {
        type: String,
    },

    address: {
        type: String,
    },

    role: {
        type: String,
    },

    isActive:{
        type: Boolean,
    },

})

</script>
