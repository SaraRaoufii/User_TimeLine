<template>
  <div class="Login Page flex justify-center bg-grayback ">
    <div class="min-h-screen Login card flex items-center">
      <el-card class="login-card w-80 p-6 m-10" shadow="hover">
        <h2 class="text-center mb-4 text-maincolor text-[40px]">Login</h2>
        <el-form :model="form" class="space-y-4" @submit.prevent="submitLogin">
          <el-input v-model="form.username" placeholder="Username" />
          <el-input v-model="form.password" type="password" placeholder="Password" />
          <el-form-item>
            <el-button
              type="primary"
              @click="submitLogin"
              class="w-full !bg-maincolor !hover:bg-lightblue !border-none text-white font-semibold py-2 rounded"
            >
              Login
            </el-button>
          </el-form-item>
        </el-form>
        <p v-if="errorMessage" class="text-darkred text-center mt-2">{{ errorMessage }}</p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAlertStore } from '@/stores/alert'

const userStore = useUserStore()
const router = useRouter()
const alertStore = useAlertStore()

const errorMessage = ref(null)
const form = reactive({
  username: '',
  password: ''
})

const LOGIN_MUTATION = gql`
  mutation TokenAuth($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
      token
      user {
        id
        username
        role
        firstName
        lastName
      }
    }
  }
`

const { mutate: login, onDone, onError } = useMutation(LOGIN_MUTATION)

const submitLogin = () => {
  errorMessage.value = null

  if (!form.username || !form.password) {
    alertStore.show('Username and password are required', 'error')
    console.warn('[Login Blocked] Empty username or password')
    return
  }

  console.log('[Login Attempt] Sending variables:', {
    username: form.username,
    password: form.password
  })

  login({ username: form.username, password: form.password }).catch(err =>
    console.error('[Mutation Error]', err)
  )
}

onDone((res) => {
  const data = res.data.tokenAuth
  if (data?.token) {
    localStorage.setItem('token', data.token)
    userStore.setUser({ ...data.user, token: data.token, refreshToken: data.refreshToken || null })

    userStore.fetchUserData()
      .then(() => {
        router.push('/')
        alertStore.show('Login successful!', 'success')
      })
      .catch(() => {
        alertStore.show('Cannot fetch user data. Please login again.', 'error')
      })
  } else {
    alertStore.show('Login failed. Please check your credentials.', 'error')
  }
})


onError((err) => {
  let msg = 'An error occurred'

  if (err.graphQLErrors?.length) {
    const gqlError = err.graphQLErrors[0].message
    try {
      const parsed = JSON.parse(gqlError)
      if (parsed.non_field_error) {
        msg = Array.isArray(parsed.non_field_error)
          ? parsed.non_field_error.join(', ')
          : parsed.non_field_error
      } else {
        const firstKey = Object.keys(parsed)[0]
        msg = Array.isArray(parsed[firstKey])
          ? parsed[firstKey].join(', ')
          : parsed[firstKey]
      }
    } catch (e) {
      msg = gqlError
    }
  }

  errorMessage.value = msg
})
</script>
