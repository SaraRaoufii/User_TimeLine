<template>
    <div class="Login Page flex justify-center bg-grayback ">
        <div class="min-h-screen Login card flex items-center  ">
            <el-card class="login-card w-80 p-6 m-10" shadow="hover">
                <h2 class="text-center mb-4 text-maincolor text-[40px]">Login</h2>
                <el-form :model="form" class="space-y-4" @submit.prevent="submitLogin">

                    <el-input v-model="form.username" placeholder="Username" />



                    <el-input v-model="form.password" type="password" placeholder="Password" />


                <el-form-item>
                    <el-button type="primary" @click="submitLogin" class="w-full !bg-maincolor !hover:bg-lightblue !border-none text-white font-semibold py-2 rounded">Login</el-button>
                </el-form-item>
                </el-form>
                <p v-if="errorMessage" class="text-darkred text-center mt-2">{{ errorMessage }}</p>
            </el-card>
        </div>
    </div>
</template>

<script setup>
import { reactive , ref} from 'vue'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user' 

    const userStore = useUserStore()
    const router = useRouter()
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
    console.log('Submitting login:', form.username, form.password)

    login({
        username: form.username,
        password: form.password
    })
    }


    onDone((res) => {
    const data = res.data.tokenAuth
    if (data?.token) {
        localStorage.setItem('token', data.token)
        userStore.setUser({ ...data.user, token: data.token })
        userStore.fetchUserData()
        router.push('/')
    } else {
        errorMessage.value = 'Login failed'
    }
    })



  onError((err) => {
    console.error('Login error:', err.message)
    errorMessage.value = 'Connect server error'
  })

</script>

