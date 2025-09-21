<template>
  <div class="edituser p-6 w-full max-w-none">

    <div class="first_row flex items-center gap-4 mb-6">
      <div class="role flex-1">
        <v-select
          v-model="form.role"
          :items="['Admin','User']"
          dense
          hide-details="auto"
          label="Role"
        ></v-select>
      </div>

      <div class="active flex-1">
        <v-switch
          v-model="form.isActive"
          dense
          hide-details="auto"
          color="green"
          label="Active"
        ></v-switch>
      </div>
    </div>


    <div class="info_items grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4">
      <div class="username">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Username:</h3>
        <v-text-field
          v-model="form.username"
          dense
          hide-details="auto"
          :rules="[v => !!v || 'Username is required.']"
          :error="!!error.username"
          :error-messages="error.username"
        ></v-text-field>
      </div>

      <div class="first_name">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">First Name:</h3>
        <v-text-field
          v-model="form.firstName"
          dense
          hide-details="auto"
          :rules="[v => !!v || 'First Name is required.']"
          :error="!!error.firstName"
          :error-messages="error.firstName"
        ></v-text-field>
      </div>

      <div class="last_name">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Last Name:</h3>
        <v-text-field
          v-model="form.lastName"
          dense
          hide-details="auto"
          :rules="[v => !!v || 'Last Name is required.']"
          :error="!!error.lastName"
          :error-messages="error.lastName"
        ></v-text-field>
      </div>

      <div class="password">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Password:</h3>
        <v-text-field
          v-model="form.password"
          type="password"
          placeholder="*********"
          dense
          hide-details="auto"
          :rules="[
            v => !!v || 'Password is required.',
            v => (v && v.length >= 8) || 'Password must be at least 8 characters.'
            ]"
          :error="!!error.password"
          :error-messages="error.password"
        ></v-text-field>
      </div>

      <div class="email">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Email:</h3>
        <v-text-field
          v-model="form.email"
          dense
          hide-details="auto"
          :rules="[
              v => !!v || 'E-mail is required.',
              v => /.+@.+\..+/.test(v) || 'E-mail must be valid.'
            ]"
          :error="!!error.email"
          :error-messages="error.email"
        ></v-text-field>
      </div>

      <div class="phonenumber">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Phone Number:</h3>
        <v-text-field
          v-model="form.phone"
          dense
          hide-details="auto"
          :rules="[
              v => !!v || 'Phone number is required.',
              v => (/^\d{11}$/.test(v)) || 'Phone number must be exactly 11 digits.'
            ]"
          :error="!!error.phone"
          :error-messages="error.phone"
        ></v-text-field>
      </div>

      <div class="address">
        <h3 class="titr text-sm font-semibold text-gray-600 mb-1 uppercase tracking-wide">Address:</h3>
        <v-text-field
          v-model="form.address"
          dense
          hide-details="auto"
          :rules="[
            v => !!v || 'Address is required.',
          ]"
          :error="!!error.address"
          :error-messages="error.address"
        ></v-text-field>
      </div>
    </div>


    <div class="btn flex flex-row gap-3 mt-6">
      <v-btn
        size="small"
        class="button bg-maincolor text-[#FEFCF4] flex items-center gap-1"
        :loading="saving"
        @click="submitForm"
      >
        <UserRoundPen class="stroke-[1.5] w-[18px] h-[18px]" />
        Save Changes
      </v-btn>

      <v-btn
        size="small"
        class="button border-maincolor text-maincolor flex items-center gap-1"
        @click="emit('cancel')"
      >
        <ArrowLeft class="stroke-[1.5] w-[18px] h-[18px]" />
        Cancel
      </v-btn>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { UserRoundPen, ArrowLeft } from 'lucide-vue-next'
import gql from 'graphql-tag'
import { useMutation } from '@vue/apollo-composable'
import { useAlertStore } from '@/stores/alert';

const alertStore = useAlertStore();
const emit = defineEmits(['saved', 'cancel'])
const error = reactive({})

const props = defineProps({
  id: String,
  username: String,
  firstName: String,
  lastName: String,
  password: String,
  phone: String,
  email: String,
  address: String,
  role: String,
  isActive: Boolean,
})

const form = reactive({
  username: props.username,
  firstName: props.firstName,
  lastName: props.lastName,
  password:"",
  phone: props.phone,
  email: props.email,
  address: props.address,
  role: props.role?.toUpperCase() || 'USER',
  isActive: props.isActive ?? true,
})

const saving = ref(false)

const UPDATE_USER = gql`
  mutation updateUser(
    $id: ID!
    $username: String
    $firstName: String
    $lastName: String
    $password: String
    $phone: String
    $email: String
    $address: String
    $role: String
    $isActive: Boolean
  ) {
    updateUser(
      id: $id
      username: $username
      firstName: $firstName
      lastName: $lastName
      password: $password
      phone: $phone
      email: $email
      address: $address
      role: $role
      isActive: $isActive
    ) {
      user {
        id
        username
        firstName
        lastName
        phone
        email
        address
        role
        isActive
      }
    }
  }
`

const { mutate: updateUser } = useMutation(UPDATE_USER)

const submitForm = async () => {
  saving.value = true

  Object.keys(error).forEach(k => error[k] = null)
    const hasChanges = Object.keys(form).some(key => {
    if (key === 'password') {
      return form.password && form.password.trim() !== ""
    }
    return form[key] !== props[key]
  })

  if (!hasChanges) {
    alertStore.show('No changes detected', 'info')
    saving.value = false
    return
  }

  try {
    const payload = { id: props.id, ...form, role: form.role.toUpperCase() }
    if (!form.password || form.password.trim() === "") {
        delete payload.password
      }

    const { data } = await updateUser(payload)
    emit('saved', data.updateUser.user)

  } catch (err) {

    if (err.graphQLErrors && err.graphQLErrors.length > 0) {
      err.graphQLErrors.forEach(e => {
        try {
          const errData = JSON.parse(e.message)
          for (const key in errData) {
            if (key in form) {
              error[key] = errData[key]
            } else if (key === 'non_field_error') {
              alertStore.show(errData[key] , 'error')
            }
          }
        } catch {
          alertStore.show(e.message , 'error')
        }
      })
    } else if (err.networkError) {
      alertStore.show('Network error' , 'error')
    } else {
      alertStore.show('Unexpected error' , 'error')
    }
  } finally {
    saving.value = false
  }
}
</script>
