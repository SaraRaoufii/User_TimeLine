<template>
  <div class="userinfo p-6 w-full max-w-none">

    <div class="first_row flex items-center gap-4 mb-6">
      <div :class="[
        'role flex justify-center items-center rounded-full w-[70px] h-[32px] px-3 font-semibold',
        props.role?.toLowerCase() === 'admin' ? 'text-maincolor bg-lightblue' : 'text-darkbrown bg-lightbrown'
      ]">
        {{ props.role || 'User' }}
      </div>

      <div :class="[
        'active flex justify-center items-center rounded-full w-[70px] h-[32px] px-3 font-semibold',
        props.isActive ? 'bg-lightgreen text-darkgreen' : 'bg-lightred text-darkred'
      ]">
        {{ props.isActive !== undefined ? (props.isActive ? 'Active' : 'Inactive') : 'Active' }}
      </div>
    </div>


    <div class="info_items ml-2 grid grid-cols-1 sm:grid-cols-2 gap-x-10 gap-y-4">
      <div class="username">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Username:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4 py-2 px-1 border-b border-gray-800 rounded-sm">{{ props.username }}</p>
      </div>

      <div class="first_name">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">First Name:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4 py-2 px-1 border-b border-gray-800 rounded-sm">{{ props.firstName }}</p>
      </div>

      <div class="last_name">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Last Name:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4 py-2 px-1 border-b border-gray-800 rounded-sm">{{ props.lastName }}</p>
      </div>

      <div class="password">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Password:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4 py-2 px-1 border-b border-gray-800 rounded-sm">
          {{  '********' }}
        </p>
      </div>

      <div class="email">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Email:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4 py-2 px-1 border-b border-gray-800 rounded-sm">{{ props.email }}</p>
      </div>

      <div class="phonenumber">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Phone Number:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4 py-2 px-1 border-b border-gray-800 rounded-sm">{{ props.phone }}</p>
      </div>

      <div class="address">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Address:</h3>
        <p class="response text-base font-medium text-gray-900 mb-4 py-2 px-1 border-b border-gray-800 rounded-sm  ">{{ props.address }}</p>
      </div>
    </div>

    <div class="btn flex flex-row gap-3 ml-2 mt-2">
      <v-btn
        size="small"
        class="button bg-maincolor text-[#FEFCF4]"
        :disabled="isAdminOtherUser"
        :class="{'opacity-50 cursor-not-allowed': isAdminOtherUser}"
        @click="emit('edit')"
      >
        <UserRoundPen class="stroke-[1.5] w-[18px] h-[18px] mr-1"/>
        Edit User
      </v-btn>

      <v-btn
        size="small"
        class="button border-darkred text-darkred"
        :disabled="isAdminOtherUser"
        :class="{'opacity-50 cursor-not-allowed': isAdminOtherUser}"
        @click="acceptDelete = true"
      >
        <UserRoundMinus class="stroke-[1.5] w-[18px] h-[18px] mr-1"/>
        Delete User
      </v-btn>

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

  </div>
</template>

<script setup>
import { UserRoundPen, UserRoundMinus } from 'lucide-vue-next';
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';
import { useAlertStore } from '@/stores/alert';
import { useMutation } from '@vue/apollo-composable';
import gql from 'graphql-tag';

const alertStore = useAlertStore();
const router = useRouter();
const props = defineProps({
  id: { type: String, required: true },
  username: { type: String, required: true },
  firstName: String,
  lastName: String,
  password: String,
  phone: String,
  email: String,
  address: String,
  role: String,
  isActive: Boolean,
});


const selectedUser = ref({
  id: props.id,
  username: props.username
});

const DELETE_USER = gql`
  mutation DeleteUser($id: ID!) {
    deleteUser(id: $id) {
      ok
    }
  }
`;
const { mutate: deleteUserMutation } = useMutation(DELETE_USER);

const handleDelete = async () => {
  if (!selectedUser.value?.id) return;

  try {
    const { data } = await deleteUserMutation({ id: selectedUser.value.id });
    if (data.deleteUser.ok) {
      alertStore.show('User deleted successfully!', 'success');
      acceptDelete.value = false;

      setTimeout(() => {
        router.push('/userslistpage'); 
      }, 800);
    } else {
      alertStore.show('Failed to delete user.', 'error');
    }
  } catch (err) {
    alertStore.show(`Delete error: ${err.message}`, 'error');
  }
};

const userStore = useUserStore();
const currentUsername = computed(() => userStore.username);


const emit = defineEmits(['edit', 'delete']);
const acceptDelete = ref(false);


const isAdminOtherUser = computed(() => props.role?.toLowerCase() === 'admin' && props.username !== currentUsername.value);
</script>
