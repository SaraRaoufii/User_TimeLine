<template>
  <div class="EditUser p-6">
    <v-form>
      <v-container>
        <v-row>
          <v-col cols="12" md="4" sm="6">
            <v-text-field
              label="Username"
              v-model="form.username"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="4" sm="6">
            <v-text-field
              label="First Name"
              v-model="form.firstName"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="4" sm="6">
            <v-text-field
              label="Last Name"
              v-model="form.lastName"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="4" sm="6">
            <v-text-field
              label="Password"
              type="password"
              v-model="form.password"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="4" sm="6">
            <v-text-field
              label="Email"
              v-model="form.email"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="4" sm="6">
            <v-text-field
              label="Phone Number"
              v-model="form.phone"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="12" sm="12">
            <v-text-field
              label="Address"
              v-model="form.address"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-btn
          color="primary"
          class="mt-4"
          @click="submitForm"
        >
          Save Changes
        </v-btn>
      </v-container>
    </v-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  username: String,
  firstName: String,
  lastName: String,
  password: String,
  phone: String,
  email: String,
  address: String,
})


const form = reactive({
  username: props.username,
  firstName: props.firstName,
  lastName: props.lastName,
  password: props.password,
  phone: props.phone,
  email: props.email,
  address: props.address,
})

const submitForm = () => {
  console.log('Updated user:', form)
}
</script>

