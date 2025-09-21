<template>
  <div class="createuser p-6 w-full max-w-none">
    <div v-if="error.non_field_error?.length" class="text-darkred mb-4 font-semibold">
      {{ error.non_field_error.join(', ') }}
    </div>
    <v-form ref="formRef">
    <div class="first_row flex items-center gap-4 mb-6">     
       <div class="role flex-1">
        <v-select
          v-model="form.role"
          :items="['Admin','User']"
          dense
          hide-details="auto"
          label="Role"
          :error="!!error.role"
          :error-messages="normalizeError(error.role)"
        />
      </div>
      <div class="active flex-1">
        <v-switch 
          v-model="form.is_active"
          dense
          hide-details="auto"
          color="green"
          label="Active"
          :error="!!error.isActive"
          :error-messages="normalizeError(error.isActive)" 
        />
        

      </div>

    </div>

    <div class="info_items grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4">
      <div class="username">
        <h3 class="titr">Username:</h3>
        <v-text-field
          v-model="form.username"
          dense
           hide-details="auto"
          :rules="[v => !!v || 'Username is required.']"
          :error="!!error.username"
          :error-messages="error.username"
        />
      </div>

      <div class="first_name">
        <h3 class="titr">First Name:</h3>
        <v-text-field
          v-model="form.firstName"
          dense
           hide-details="auto"
          :rules="[v => !!v || 'First Name is required.']"
          :error="!!error.firstName"
          :error-messages="error.firstName"
        />
      </div>

      <div class="last_name">
        <h3 class="titr">Last Name:</h3>
        <v-text-field
          v-model="form.lastName"
          dense
           hide-details="auto"
          :rules="[v => !!v || 'Last Name is required.']"
          :error="!!error.lastName"
          :error-messages="error.lastName"
        />
      </div>

      <div class="password">
        <h3 class="titr">Password:</h3>
        <v-text-field
          v-model="form.password"
          type="password"
          dense
           hide-details="auto"
            :rules="[
              v => !!v || 'Password is required.',
              v => (v && v.length >= 8) || 'Password must be at least 8 characters.'
            ]"
          :error="!!error.password"
          :error-messages="error.password"
        />
      </div>

      <div class="email">
        <h3 class="titr">Email:</h3>
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
        />
      </div>

      <div class="phonenumber">
        <h3 class="titr">Phone Number:</h3>
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
        />
      </div>

      <div class="address">
        <h3 class="titr">Address:</h3>
        <v-text-field
          v-model="form.address"
          dense
           hide-details="auto"
           :rules="[
            v => !!v || 'Address is required.',
          ]"
          :error="!!error.address"
          :error-messages="error.address"
        />
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
        Save User
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
    </v-form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { UserRoundPen, ArrowLeft } from 'lucide-vue-next';
import gql from 'graphql-tag';
import { useMutation } from '@vue/apollo-composable';
import { useRouter } from 'vue-router';
import { useAlertStore } from '@/stores/alert';

const alertStore = useAlertStore();
const emit = defineEmits(['saved', 'cancel']);
const router = useRouter();
const formRef = ref(null);

const form = reactive({
  username: '',
  firstName: '',
  lastName: '',
  password: '',
  phone: '',
  email: '',
  address: '',
  role: 'User',
  is_active: true,
});

const saving = ref(false);

const CREATE_USER = gql`
  mutation createUser(
    $username: String!
    $firstName: String!
    $lastName: String!
    $password: String!
    $phone: String
    $email: String
    $address: String
    $role: String
    $isActive: Boolean
  ) {
    createUser(
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
`;

const { mutate: createUser } = useMutation(CREATE_USER);

const error = reactive({
  username: null,
  firstName: null,
  lastName: null,
  password: null,
  phone: null,
  email: null,
  address: null,
  role: null,
  isActive: null,
  non_field_error: null,
});

const errorKeyMap = {
  username: 'username',
  firstName: 'firstName',
  lastName: 'lastName',
  password: 'password',
  phone: 'phone',
  email: 'email',
  address: 'address',
  role: 'role',
  is_active: 'isActive',
  isActive: 'isActive',
  non_field_error: 'non_field_error',
  non_field_errors: 'non_field_error',
};

const normalizeError = (val) => {
  if (!val) {
    return [];
  }

  if (Array.isArray(val)) {
    return val;
  }

  if (typeof val === 'string') {
    try {
      const parsedVal = JSON.parse(val);
      if (Array.isArray(parsedVal)) {
        return parsedVal;
      }
      if (typeof parsedVal === 'object' && parsedVal !== null) {
        return Object.values(parsedVal).flat();
      }
    } catch {
    }
  }
  return [val];
};

const submitForm = async () => {
  saving.value = true;
  Object.keys(error).forEach(k => (error[k] = null));
  const { valid } = await formRef.value.validate();
  if (!valid) {
    saving.value = false;
    return;
  }

  try {
    const { data } = await createUser({
      ...form,
      role: form.role.toUpperCase(),
    });
    alertStore.show('User Create', 'success');
    router.push('/userslistpage');
    emit('saved', data.createUser);
  } catch (err) {
  if (err.graphQLErrors && err.graphQLErrors.length > 0) {
    err.graphQLErrors.forEach(e => {
      try {
        const errData = JSON.parse(e.message)
        for (const key in errData) {
          if (key in form) {
            error[key] = normalizeError(errData[key])
          } else if (key === 'non_field_error' || key === 'non_field_errors') {
            alertStore.show(normalizeError(errData[key]).join(', '), 'error')
          }
        }
      } catch {
        alertStore.show(e.message, 'error')
      }
    })
  } else if (err.networkError) {
    alertStore.show('Network error', 'error')
  } else {
    alertStore.show('Unexpected error', 'error')
  }
}
 finally {
    saving.value = false;
  }
};
</script>